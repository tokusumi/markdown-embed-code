from os import getuid
from pathlib import Path
from subprocess import run

from git import Actor, Repo
from pydantic import BaseSettings, SecretStr

from markdown_embed_code import render_markdown_file


class MissingRefError(Exception):
    ...


class Settings(BaseSettings):
    github_actor: str
    github_head_ref: str
    github_ref: str
    github_repository: str
    github_workspace: Path
    input_markdown: str = "README.md"
    input_message: str = "Embed code into Markdown."
    input_token: SecretStr


def main(settings: Settings):
    ref = settings.github_head_ref or settings.github_ref

    if not ref:
        raise MissingRefError()

    workspace = Path(settings.github_workspace)

    # WORKAROUND: The checkout action clones the repo out as the runner user (id 1001) and our
    # container / script runs as root, as recommended by the actions documentation.
    # The below ensures that this script has permission to do its work.
    run(
        f"chown -R $(id -u) {workspace}",
        check=True,
        shell=True,
    )

    glob_pattern = f"{settings.input_markdown}/*.md" if (workspace / settings.input_markdown).is_dir() else settings.input_markdown

    for file_path in Path(workspace).glob(glob_pattern):
        render_markdown_file(file_path)

    repo = Repo(workspace)
    repo.remotes.origin.set_url(
        f"https://{settings.github_actor}:{settings.input_token.get_secret_value()}@github.com/{settings.github_repository}.git"
    )
    repo.index.add([glob_pattern])

    if repo.is_dirty(untracked_files=True):
        repo.index.commit(
            settings.input_message,
            author=Actor(
                name=settings.github_actor,
                email=f"{settings.github_actor}@github.com",
            ),
        )
        repo.remotes.origin.push(f"HEAD:{ref}").raise_if_error()
    else:
        print("No changes to commit.")


if __name__ == "__main__":
    settings = Settings()
    main(settings)
