# Automation playbook to deploy Django application on AWS EC2 instance using Docker

This automation playbook is used to create/delete AWS EC2 instance on which a Django application
will be deployed.

## Requirements

---

- AWS User Account with valid permission.

# Playbook variables

---

## AWS credentials variables

- _aws_profile_: AWS profile to use.
- _aws_access_key_id_: AWS access key id.
- _aws_secret_access_key_: AWS secret key id.
- _aws_security_token_: AWS security token.
- _aws_region_: AWS region, default to `us-east-1`.

## Application variables

- _resource_prefix_: Prefix of AWS resource to create.
- _node_port_: Application listening port on EC2 instance. default to `30090`.
- _github_token_: Github token.

# How to deploy the application

---

The application is deployed using the following command:

```shell
ANSIBLE_INVENTORY_ENABLED="amazon.aws.aws_ec2" ANSIBLE_INVENTORY=inventory.aws_ec2.yml ansible-playbook play.yaml -e "@vars.yaml" -v
```
