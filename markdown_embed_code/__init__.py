from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from marko import Markdown
from marko.md_renderer import MarkdownRenderer


@dataclass
class Embed:
    file_path: Path
    start_line: int
    end_line: Optional[int]

    @classmethod
    def from_string(cls, embed_string: str) -> Embed:
        path, *other = re.split(r"\[([\d\s\-:]*)\]", embed_string)
        line_range, *_ = other or ["1"]
        start, end = (re.split(r"-|:", line_range) + [""])[:2]

        return cls(
            file_path=Path(path.strip()),
            start_line=int(start) or 1,
            end_line=int(end) if end else None,
        )

    def get_code(self) -> str:
        with self.file_path.open() as file:
            code = "".join(file.readlines()[self.start_line - 1:self.end_line])

            return f"{code}\n" if code[-1] != "\n" else code


class MarkdownEmbCodeRenderer(MarkdownRenderer):
    def render_fenced_code(self, element):
        lang = element.__dict__.get("lang")
        lang, *options = lang.rsplit(":", 1)

        if options:
            option = options[0]

            if element.__dict__.get("extra"):
                option += element.__dict__.get("extra")

            element.children[0].children = Embed.from_string(option).get_code()

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
