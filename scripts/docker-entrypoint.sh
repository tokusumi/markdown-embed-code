#!/usr/bin/env sh

set -e

#exec su -c "python -m markdown_embed_code" $(stat -c %U $GITHUB_WORKSPACE)
stat -c %U $GITHUB_WORKSPACE
