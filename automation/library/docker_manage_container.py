#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2023, Aubin BIKOUO <@abikouo>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: docker_manage_container

short_description: Start/Restart or stop a container application using a specific image.

author:
    - "Aubin BIKOUO (@abikouo)"

description:
  - Locate existing running container by name.
  - start or stop container using input parameters.

options:
  state:
    description:
    - Whether to start or stop the container.
    choices:
    - present
    - absent
    default: present
    type: str
  container_image:
    description:
    - The container image.
    - Required when starting a container.
    type: str
  container_name:
    description:
    - The container name.
    type: str
    required: true
    aliases:
    - name
  env_vars:
    description:
    - The list of environment variables to set when running the container.
    type: list
    elements: str
  container_port:
    description:
    - The port exposed on the container.
    type: int
  node_port:
    description:
    - The node port to bind with the container port.
    type: int
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import subprocess
from ansible.module_utils.basic import AnsibleModule
import json


def check_container(container_name):
    command = ["docker", "inspect", container_name]
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = cmd.communicate()

    result = {}
    if cmd.returncode == 0:
        result = json.loads(out)[0]

    return result


def run_command(command):
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = cmd.communicate()
    return out, err, cmd.returncode


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=["present", "absent"]),
            container_image=dict(),
            container_name=dict(type="str", required=True),
            env_vars=dict(type="list", elements="str", default=[]),
            container_port=dict(type="int"),
            node_port=dict(type="int"),
        ),
        required_if=[("state", "present", ["container_image"])],
    )

    # check if container exists
    container_name = module.params.get("container_name")
    existing = check_container(container_name)
    changed = False
    if existing:
        # delete running container
        command = ["docker", "container", "rm", "-f", existing["Id"]]
        out, err, rc = run_command(command)
        if rc != 0:
            module.fail_json(msg=err, stdout=out, rc=rc)
        changed = True

    state = module.params.get("state")

    if state == "present":
        command = ["docker", "run", "-d", "--restart=always", "--name", container_name]
        node_port = module.params.get("node_port")
        container_port = module.params.get("container_port")
        if node_port and container_port:
            command.extend(["-p", "{0}:{1}".format(node_port, container_port)])
        env_vars = module.params.get("env_vars", [])
        for env in env_vars:
            command.extend(["--env", env])
        command.append(module.params.get("container_image"))
        out, err, rc = run_command(command)
        if rc != 0:
            module.fail_json(msg=err, stdout=out, rc=rc)
        changed = True

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
