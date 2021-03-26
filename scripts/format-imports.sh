#!/bin/sh -e
set -x

isort markdown_embed_code tests scripts 
sh ./scripts/format.sh