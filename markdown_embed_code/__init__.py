from __future__ import annotations

from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from re import match
from typing import Iterator, Optional

from marko import Markdown
from marko.md_renderer import MarkdownRenderer


def slice_file(
    file_path: Path,
    start_at: int = 1,
    end_at: Optional[int] = None,
) -> Iterator[str]:
    with file_path.open() as file:
        for line in islice(file, start_at - 1, end_at):
            yield f"{line}\n" if line[-1] != "\n" else line


@dataclass
class Embed:
    file_path: Path
    start_at: int
    end_at: Optional[int]

    @classmethod
    def from_string(cls, file_path: str) -> Embed:
        try:
            pattern = r"\s*(?P<file_path>.+\S)(?:\s*\[\s*(?P<start_at>\d+)\s*(?:-|:|,)?\s*(?P<end_at>\d*)?\s*\])"
            file_path, start_at, end_at = match(pattern, file_path).group("file_path", "start_at", "end_at")
        except AttributeError:
            start_at, end_at = 1, None

        return cls(
            file_path=Path(file_path),
            start_at=int(start_at) or 1,
            end_at=int(end_at) if end_at else None,
        )

    @property
    def code(self) -> str:
        return ''.join(slice_file(**self.__dict__))


class MarkdownEmbCodeRenderer(MarkdownRenderer):
    def render_fenced_code(self, element):
        if element.__dict__["extra"]:
            element.children[0].children = Embed.from_string(element.__dict__["extra"]).code

        return super().render_fenced_code(element)

    def render_image(self, element):
        template = "![{}]({}{})"
        title = (
            ' "{}"'.format(element.title.replace('"', '\\"')) if element.title else ""
        )
        return template.format(self.render_children(element), element.dest, title)


_markdown = Markdown(renderer=MarkdownEmbCodeRenderer)


def render(document: str):
    return _markdown(document)
