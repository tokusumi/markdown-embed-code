#!/usr/bin/env sh

set -e

exec su -c "python -m markdown_embed_code" $(stat -c %u $GITHUB_WORKSPACE)
