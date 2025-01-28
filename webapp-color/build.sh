#!/bin/bash
tstamp="$(date '+%Y%m%d_%H%M%S')"
docker build -t "akslab88lu9i.azurecr.io/webapp-color:${tstamp}" .
docker push akslab88lu9i.azurecr.io/webapp-color:${tstamp}