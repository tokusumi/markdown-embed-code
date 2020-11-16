# markdown-embed-code

Embedding code into markdown from external file.
Any language's code blocks are available.

## How to use

In markdown, write code block as follows:

```markdown
　```python:tests/src/sample.py
　
　```
```

Then, this action referes to `tests/src/sample.py` and modifies markdown as (if something code is written, they are overridden):

```markdown
　```python:tests/src/sample.py
  from math import sqrt


  def sample(x):
      return sqrt(x)

　```
```

NOTE: Read file by passed path, where the top directory in your repo is working directory. If the path is wrong, this action is failed.

### How to use - workflow example

Override README.md and push by action:

```yaml
name: Embed code in README

on:
  pull_request:
    branches:
      - main

jobs:
  embed-code:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: tokusumi/markdown-embed-code@main
        with:
          markdown: "README.md"
      - name: Commit files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git commit -m "Embedding code into Markdown" -a
      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: ${{ github.ref }}
```
