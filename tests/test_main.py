import pytest

from markdown_embed_code import get_code_emb


def test_embed_code_from_file():
    """```[lang]:[filepath] are available."""
    text = """```python:tests/src/sample.py\n```\n"""
    code_emb = get_code_emb()
    assert code_emb(text) == (
        "```python:tests/src/sample.py\n"
        "from math import sqrt\n"
        "\n"
        "\n"
        "def sample(x):\n"
        "    return sqrt(x)\n"
        "\n"
        "```\n"
    )


def test_override_embed_code_from_file():
    """```[lang]:[filepath] are available."""
    text_contains_code = (
        """```python:tests/src/sample.py\nprint('code already exists')\n```\n"""
    )
    code_emb = get_code_emb()
    assert code_emb(text_contains_code) == (
        "```python:tests/src/sample.py\n"
        "from math import sqrt\n"
        "\n"
        "\n"
        "def sample(x):\n"
        "    return sqrt(x)\n"
        "\n"
        "```\n"
    ), "Must override code in text"


def test_ignore_no_filepath():
    """if no filepath, ignore them."""
    text = """```python\n```\n"""
    code_emb = get_code_emb()
    assert text == code_emb(text)


@pytest.mark.parametrize(
    "lang",
    [
        "python:tests/src/sample.py[4-6]",
        "python:tests/src/sample.py [4-6]",
    ],
)
def test_embed_code_only_specific_line_from_file(lang):
    """```[lang]:[filepath] [line no] are available."""
    code_emb = get_code_emb()
    text_contains_code = f"""```{lang}\n```\n"""
    # fmt:off
    assert code_emb(text_contains_code) == (
        f"```{lang}\n"
        "def sample(x):\n"
        "    return sqrt(x)\n"
        "\n"
        "```\n"
    ), "Must contain selected lines in code in text"
    # fmt:on


def test_embed_code_only_specific_line_from_file_2():
    """```[lang]:[filepath] [line no] are available."""
    text_code = """```python:tests/src/sample.py[4-]\n```\n"""

    code_emb = get_code_emb()
    assert code_emb(text_code) == (
        "```python:tests/src/sample.py[4-]\n"
        "def sample(x):\n"
        "    return sqrt(x)\n"
        "\n"
        "```\n"
    ), "Must contain selected lines in code in text"

    text_code = """```python:tests/src/sample.py[-3]\n```\n"""
    code_emb = get_code_emb()
    # fmt:off
    assert code_emb(text_code) == (
        "```python:tests/src/sample.py[-3]\n"
        "from math import sqrt\n"
        "\n"
        "\n"
        "```\n"
    ), "Must contain selected lines in code in text"
    # fmt:on
