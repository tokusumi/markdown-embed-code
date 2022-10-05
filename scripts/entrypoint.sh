#!/usr/bin/env sh

set -e

exec sudo -u $(stat -c %U $GITHUB_WORKSPACE) python -m markdown_embed_code
