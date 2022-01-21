import subprocess
import sys
from pathlib import Path
from typing import Optional

from github import Github
from pydantic import BaseModel, BaseSettings, SecretStr
from urllib.parse import urlparse

from markdown_embed_code import get_code_emb


class Settings(BaseSettings):
    input_markdown: Path = Path("README.md")
    input_message: str = "📝 Update Readme"
    input_no_change: str = "No changes on README!"
    input_output: Path = Path("")
    input_silent: bool = False
    input_token: SecretStr
    input_server: str
    github_actor: str
    github_repository: str
    github_event_name: str
    github_event_path: Path


class PartialGitHubEventInputs(BaseModel):
    number: int


class PartialGitHubEvent(BaseModel):
    ref: Optional[str] = None
    number: Optional[int] = None
    inputs: Optional[PartialGitHubEventInputs] = None


settings = Settings()
subprocess.run(["git", "config", "--local", "user.name", "github-actions"], check=True)
subprocess.run(
    ["git", "config", "--local", "user.email", "github-actions@github.com"], check=True
)

g = Github(base_url=f"{settings.input_server}/api/v3", login_or_token=settings.input_token.get_secret_value())
repo = g.get_repo(settings.github_repository)
if not settings.github_event_path.is_file():
    sys.exit(1)
contents = settings.github_event_path.read_text()
event = PartialGitHubEvent.parse_raw(contents)

ref = None

if settings.github_event_name == 'pull_request':
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
    ref = pr.head.ref
elif settings.github_event_name == 'push':
    ref = event.ref

if not ref:
    print('unknown ref', ref)
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


proc = subprocess.run(
    ["git", "status", "--porcelain"], check=True, stdout=subprocess.PIPE
)
if not proc.stdout:
    # no change
    if not settings.input_silent:
        pr.create_issue_comment(settings.input_no_change)
    sys.exit(0)

subprocess.run(["git", "add", output_path], check=True)
subprocess.run(["git", "commit", "-m", settings.input_message], check=True)

remote_repo = f"https://{settings.github_actor}:{settings.input_token.get_secret_value()}@{urlparse(settings.input_server).hostname}/{settings.github_repository}.git"
proc = subprocess.run(["git", "push", remote_repo, f"HEAD:{ref}"], check=False)
if proc.returncode != 0:
    sys.exit(1)
