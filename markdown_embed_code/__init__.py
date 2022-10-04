from __future__ import annotations

import itertools
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

from marko import Markdown
from marko.md_renderer import MarkdownRenderer

Lines = Iterator[str]


def slice_file(
    file_path: Path,
    start_at: int = 1,
    end_at: Optional[int] = None,
) -> Lines:
    with file_path.open() as file:
        for line in itertools.islice(file, start_at - 1, end_at):
                yield f"{line}\n" if line[-1] != "\n" else line


@dataclass
class Embed:
    file_path: Path
    start_at: int
    end_at: Optional[int]

    @classmethod
    def from_string(cls, path: str) -> Embed:
        try:
            start_at, end_at = 1, None
            path, start_at, end_at = re.match(r"(.*)\[\s*(\d*)?\s*(?:-|:|,)?\s*(\d*)?\s*\]", path).group(1, 2, 3)
        except AttributeError:
            pass

        return cls(
            file_path=Path(path.strip()),
            start_at=int(start_at or 1) or 1,
            end_at=int(end_at) if end_at else None,
        )

    @property
    def code(self) -> str:
        return ''.join(slice_file(**self.__dict__))


class MarkdownEmbCodeRenderer(MarkdownRenderer):
    def render_fenced_code(self, element):
        extra_options = element.__dict__["extra"]
        if extra_options:
            element.children[0].children = Embed.from_string(extra_options).code

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
