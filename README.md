# markdown-embed-code

Embedding code into markdown from external file.
Any language's code blocks are available.

See [demo repo](https://github.com/tokusumi/readme-code-testing) if you are interested in testing code within README.

## How to use

In markdown, write code block as follows:

````markdown
```python:tests/src/sample.py

```

And, you can refer specific lines as
```python:tests/src/sample.py [4-5]

```
````

Then, this action referes to `tests/src/sample.py` and modifies markdown as (if something code is written, they are overridden):

```python:tests/src/sample.py
from math import sqrt


def sample(x):
    return sqrt(x)

```

And, specific lines is refered as

```python:tests/src/sample.py [4-5]
def sample(x):
    return sqrt(x)
```

NOTE: Read file by passed path, where the top directory in your repo is working directory. If the path is wrong, this action is failed.

### How to use - workflow example

Override README.md and push by action if readme is changed:

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
        with:
          persist-credentials: false # otherwise, the token used is the GITHUB_TOKEN, instead of your personal token
          fetch-depth: 0 # otherwise, you will failed to push refs to dest repo
          ref: ${{ github.head_ref }}

      - uses: tokusumi/markdown-embed-code@main
        with:
          markdown: "README.md"
          token: ${{ secrets.GITHUB_TOKEN }}
          message: "synchronizing Readme"
          silent: true
```

### Configuration

| input                | description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| token                | Token for the repo. Can be passed in using {{ secrets.GITHUB_TOKEN }}   |
| markdown (Optional)  | Target markdown file path. (default: "README.md")                       |
| message (Optional)   | Commit message for action. (default: "Embedding code into Markdown")    |
| no_change (Optional) | Issue comment at no changed (default: "No changes on README!" )         |
| output (Optional)    | Output markdown file path. If none, override target file. (default: "") |
| silent (Optional)    | No issue comment in silent mode (default: false)                        |
| server (Optional)    | GitHub server URL (default: https://github.com)                         |
