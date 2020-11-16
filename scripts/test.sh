#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
ROOT=$SCRIPT_DIR/../

cd ROOT
pytest .