# markdown-embed-code

Forked from [https://github.com/tokusumi/readme-code-testing](https://github.com/tokusumi/readme-code-testing) and partially rewritten with some fixes, some features added, some removed.

Allows you to "import" code into your markdown files from elsewhere in your repository without having to manually copy and paste.
Supports code blocks in any language. Your original markdown file(s) will be overwritten with the rendered content.

<!-- See [demo repo](https://github.com/tokusumi/readme-code-testing) if you are interested in testing code within README. -->

## Usage

### Embedding Entire files

In markdown, reference your file as follows in an otherwise empty code block.

````markdown
```python:tests/src/sample.py

```
````

The action reads in the content from `tests/src/sample.py` and inserts its contents into your code block like so:

```python:tests/src/sample.py
from math import sqrt


def sample(x):
    return sqrt(x)

```

Any contents within your code block will be overwritten. Paths are relative to the root of your repository and not the directory containing the file being processed.

### Embedding Snippets

You can pull in a snippet from a file by including a range of line numbers like so:

````markdown
```python:tests/src/sample.py [4-5]

```
````

Which will render the following output.

```python:tests/src/sample.py [4-5]
def sample(x):
    return sqrt(x)
```

### Workflow setup

Process README.md, import any referenced code, and push to your repo if there are any changes.

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
      - uses: actions/checkout@v3
        with:
          persist-credentials: false # otherwise, the token used is the GITHUB_TOKEN, instead of your personal token
          fetch-depth: 0 # otherwise, you will failed to push refs to dest repo
          ref: ${{ github.head_ref }}

      - uses: analogous-structures-labs/markdown-embed-code@main
        with:
          markdown: "README.md"
          message: "Synchronize Readme."
          token: ${{ secrets.GITHUB_TOKEN }}
```

### Configuration

| input                | description                                                              |
| -------------------- | ------------------------------------------------------------------------ |
| token                | Token for the repo. Can be passed in using `{{ secrets.GITHUB_TOKEN }}`. |
| markdown (Optional)  | Target path for your markdown file(s). (default: "README.md")            |
| message (Optional)   | Commit message for action. (default: "Embed code into Markdown.")        |


### Specifying your markdown path

The value provided for the `markdown` parameter supports specifying directories and glob patterns.
"README.md" will process only the top level README.
"some_dir" will process any files in some_dir with .md as their file extension.
"some_dir/README.md" will process only the README file within some_dir.
"\*\*/README.md" will process any markdown files named README.md, recursively through your repository.
"\*\*/*.md" will process any markdown files with .md as their file extension, recursively through your repository.
