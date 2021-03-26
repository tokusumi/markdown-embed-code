#!/usr/bin/env bash

set -e
set -x

flake8 markdown_embed_code tests
black markdown_embed_code tests --check
isort markdown_embed_code tests scripts --check-only