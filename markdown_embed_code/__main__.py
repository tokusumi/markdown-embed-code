from pathlib import Path

from pydantic import BaseSettings

from markdown_embed_code import get_code_emb


class Settings(BaseSettings):
    input_markdown: Path = Path("README.md")
    input_output: Path = Path("")


settings = Settings()

with open(settings.input_markdown, "r") as f:
    doc = f.read()

md = get_code_emb()
embedded_doc = md(doc)

if not settings.input_output.is_dir():
    output_path = settings.input_output
else:
    output_path = settings.input_markdown

with open(output_path, "w") as f:
    f.write(embedded_doc)
