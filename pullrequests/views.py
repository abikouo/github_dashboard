from django.shortcuts import render
from django.http import Http404
from pathlib import PosixPath
import logging
import os
import yaml
from github import Github
from datetime import datetime, timedelta
from functools import wraps
from hashlib import sha256
import requests


FORMAT = "[%(asctime)s] - %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def params_digest(*args, **kwargs):

    hash_key = sha256()
    for arg in args:
        data = "{0}".format(arg)
        hash_key.update(data.encode())

    for k, v in kwargs.items():
        data = "{0}: {1}".format(k, v)
        hash_key.update(data.encode())

    return hash_key.hexdigest()


def cache(ttl=timedelta(minutes=30)):
    cache = {}

    def inner(func):
        @wraps(func)
        def caller(*args, **kwargs):
            now = datetime.now()
            key = params_digest(func.__name__, *args, **kwargs)
            if key not in cache or (now - cache[key]["time"]) > ttl:
                cache[key] = {"time": now, "value": func(*args, **kwargs)}
            return cache[key]["value"]

        return caller

    return inner


@cache(timedelta(hours=4))
def read_config():
    logger.info("Going to read cache config")
    root = os.path.dirname(os.path.abspath(__file__))
    logger.info("Running from path => '%s'", os.getcwd())
    config_file_path = PosixPath(os.path.join(root, "config.yaml"))
    if not config_file_path.exists():
        raise Http404("Missing configuration file 'config.yaml'")

    with config_file_path.open() as fd:
        config_data = list(yaml.safe_load_all(fd))
        logger.info("Configuration data => %s", config_data)
        return config_data[0]


def compute_age(created_at):
    delta = datetime.now() - created_at
    return str(delta).split(".", maxsplit=1)[0]


def pr_to_dict(pr):
    return {
        "created_at": pr.created_at,
        "age_days": (datetime.utcnow() - pr.created_at).days,
        "age": compute_age(pr.created_at),
        "changed_files": pr.changed_files,
        "title": pr.title,
        "base": pr.base.ref,
        "link": pr.html_url,
        "author": pr.user.login,
        "reviews": get_reviews(pr),
        "id": pr.number,
    }


def get_reviews(pr):
    endpoint_url = pr.url + "/reviews"
    response = requests.get(
        endpoint_url,
        headers={"Authorization": "Bearer %s" % os.environ.get("GITHUB_TOKEN")},
    )
    reviews = sorted(
        [
            {
                "author": rev["user"]["login"],
                "submitted_at": datetime.fromisoformat(
                    rev["submitted_at"].replace("Z", "+00:00")
                ),
                "state": rev["state"],
            }
            for rev in response.json()
            if rev["user"]["login"] != pr.user.login
        ],
        key=lambda d: d["submitted_at"],
    )

    # Calculate the final review state for each reviewer
    user_reviews = {}
    for rev in reviews:
        user_reviews[rev["author"]] = rev["state"]
    return [{"state": value.lower(), "user": key} for key, value in user_reviews.items()]


@cache(timedelta(minutes=30))
def get_pull_requests(repository, users):

    access_token = os.environ.get("GITHUB_TOKEN")
    gh_client = Github(access_token)
    gh_repository = gh_client.get_repo(repository)

    pulls = gh_repository.get_pulls(state="open")
    return [pr for pr in pulls if pr.user.login in users], len(list(pulls))



def index(request):

    config = read_config()
    collections = []
    now = datetime.utcnow()
    for item in config.get("collections"):
        team_prs, total_prs = get_pull_requests(item, config.get("users"))
        collections.append(
            {
                "short_name": item.split("/")[1],
                "name": item,
                "number_prs": len(team_prs),
                "total_prs": total_prs,
                "recent_prs": len([pr for pr in team_prs if (now - pr.created_at).days == 0]),
            }
        )

    logger.info("collections => %s", collections)
    context = {
        "collections": collections,
        "summary": {
            "number_prs": sum([item.get("number_prs") for item in collections]),
            "recent_prs": sum([item.get("recent_prs") for item in collections]),
            "total_prs": sum([item.get("total_prs") for item in collections]),
        },
    }
    return render(request, "pullrequests/index.html", context)


def display(request, repository_name):

    config = read_config()
    full_name = None
    for item in config.get("collections"):
        if repository_name == item.split("/")[1]:
            full_name = item
            break
    if not full_name:
        raise Http404("Unable to determine repository full name from short name -> %s" % repository_name)

    logger.info("reading pull requests for repository => %s", full_name)
    team_prs, _ = get_pull_requests(full_name, config.get("users"))
    pullreq_info = sorted([pr_to_dict(pr) for pr in team_prs], key=lambda item: item["created_at"])
    logger.info("pull requests details => %s", pullreq_info)
    context = {
        "pullrequests": pullreq_info,
        "repository_name": full_name,
    }
    return render(request, "pullrequests/display.html", context)
