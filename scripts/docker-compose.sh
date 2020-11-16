#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
ROOT=$SCRIPT_DIR/../

cd ROOT
docker-compose -f scripts/docker-compose.yml up
docker-compose -f scripts/docker-compose.yml down
