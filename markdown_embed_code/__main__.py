import subprocess
import sys
from pathlib import Path
from typing import List

from pydantic import BaseSettings, SecretStr

from markdown_embed_code import render


class Settings(BaseSettings):
    github_actor: str
    github_head_ref: str
    github_ref: str
    github_repository: str
    input_markdown: str = "README.md"
    input_message: str = "Embed code into Markdown."
    input_token: SecretStr


def run_command(command: List, **kwargs):
    return subprocess.run(
        command,
        check=True,
        **kwargs,
    )


def overwrite_file(file_handle, new_contents):
    file_handle.seek(0)
    file_handle.write(new_contents)
    file_handle.truncate()


settings = Settings()

# The checkout action checks out code as the runner user (1001:121). Our docker image runs as root
# as recommended by the GitHub actions documentation. For that reason, we're ensuring he the user
# running the script owns the workspace. Otherwise, the subsequent git commands will fail.
run_command("chown -R $(id -u):$(id-g) .", shell=True)

run_command(["git", "config", "--local", "user.name", "github-actions"])
run_command(["git", "config", "--local", "user.email", "github-actions@github.com"])

ref = settings.github_head_ref or settings.github_ref

if not ref:
    sys.exit(1)

if Path(settings.input_markdown).is_dir():
    settings.input_markdown = f'{settings.input_markdown}/*.md'

for file_path in Path(".").glob(settings.input_markdown):
    with file_path.open("r+") as file:
        overwrite_file(file, render(file.read()))
        run_command(["git", "add", file_path])

git_status_output = run_command(
    ["git", "status", "--porcelain"],
    stdout=subprocess.PIPE,
).stdout

if git_status_output:
    run_command(["git", "commit", "-m", settings.input_message])
    remote_repo = f"https://{settings.github_actor}:{settings.input_token.get_secret_value()}@github.com/{settings.github_repository}.git"
    run_command(["git", "push", remote_repo, f"HEAD:{ref}"])
else:
    print("No changes to commit.")
