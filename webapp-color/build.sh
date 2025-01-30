#!/bin/bash
if [ -z "${1}" ]; then
  tag="$(date '+%Y%m%d_%H%M%S')"
else
  tag="${1}"
fi
docker build -t "akslab88lu9i.azurecr.io/webapp-color:${tag}" .
docker push "akslab88lu9i.azurecr.io/webapp-color:${tag}"
