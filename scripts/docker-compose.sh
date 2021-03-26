#!/bin/bash

set -x

docker-compose -f scripts/docker-compose.yml up --build
docker-compose -f scripts/docker-compose.yml down
