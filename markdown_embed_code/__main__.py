from typing import Optional
import sys
from pathlib import Path
import subprocess

from pydantic import BaseSettings, SecretStr, BaseModel
from github import Github

from markdown_embed_code import get_code_emb


class Settings(BaseSettings):
    input_markdown: Path = Path("README.md")
    input_message: str = "📝 Update Readme"
    input_no_change: str = "No changes on README!"
    input_output: Path = Path("")
    input_token: SecretStr
    github_repository: str
    github_event_path: Path


class PartialGitHubEventInputs(BaseModel):
    number: int


class PartialGitHubEvent(BaseModel):
    number: Optional[int] = None
    inputs: Optional[PartialGitHubEventInputs] = None


settings = Settings()
subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)


g = Github(settings.input_token.get_secret_value())
repo = g.get_repo(settings.github_repository)
if not settings.github_event_path.is_file():
    sys.exit(1)
contents = settings.github_event_path.read_text()
event = PartialGitHubEvent.parse_raw(contents)
if event.number is not None:
    number = event.number
elif event.inputs and event.inputs.number:
    number = event.inputs.number
else:
    sys.exit(1)
pr = repo.get_pull(number)
if pr.merged:
    # ignore at merged
    sys.exit(0)

if not settings.input_output.is_dir():
    output_path = settings.input_output
else:
    output_path = settings.input_markdown

with open(settings.input_markdown, "r") as f:
    doc = f.read()

md = get_code_emb()
embedded_doc = md(doc)

with open(output_path, "w") as f:
    f.write(embedded_doc)

proc = subprocess.run(["git", "status", "--porcelain", "|", "wc", "-l"], check=True)
if proc.returncode != 0:
    # no change
    pr.create_issue_comment(settings.input_no_change)
    sys.exit(0)

subprocess.run(["git", "add", output_path], check=True)
subprocess.run(["git", "commit", "-m", settings.input_message], check=True)
subprocess.run(["git", "push"], check=True)
