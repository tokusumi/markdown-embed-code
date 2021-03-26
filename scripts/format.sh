#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --in-place markdown_embed_code tests scripts
black markdown_embed_code tests scripts
isort markdown_embed_code tests scripts