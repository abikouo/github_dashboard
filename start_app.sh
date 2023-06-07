#!/bin/sh

set -o errexit

# create application container unless it already exists
container_image=$1
container_env_file=$2
container_name='github-app'
container_port='80'
if [ "$(docker inspect -f '{{.State.Running}}' "${container_name}" 2>/dev/null || true)" != 'true' ]; then
  docker run \
    --env-file ${container_env_file} \
    -d --restart=always \
    -p "${container_port}:8000" --name "${container_name}" \
    ${container_image}
fi