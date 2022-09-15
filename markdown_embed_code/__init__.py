from pathlib import Path
from typing import Optional, Tuple

from marko import Markdown
from marko.md_renderer import MarkdownRenderer


def parse(option: str) -> Tuple[Path, int, Optional[int]]:
    file, *options = option.split("[", 1)
    file_path = Path(file.strip())

    if options:
        option = options[0]
        range_, *_ = option.split("]", 1)
        idxs = [f.strip() for f in range_.split("-", 1)]

        if len(idxs) == 1:
            start = 0 if not idxs[0] else int(idxs[0]) - 1
            return file_path, start, None
        elif len(idxs) == 2:
            start = 0 if not idxs[0] else int(idxs[0]) - 1
            end = None if not idxs[1] else int(idxs[1])
            return file_path, start, end

    return file_path, 0, None


class MarkdownEmbCodeRenderer(MarkdownRenderer):
    def render_fenced_code(self, element):
        lang = element.__dict__.get("lang")
        lang, *options = lang.rsplit(":", 1)

        if not options:
            return super().render_fenced_code(element)

        option = options[0]

        if element.__dict__.get("extra"):
            option += element.__dict__.get("extra")

        file_path, start, end = parse(option)

        with file_path.open() as f:
            if start == 0 and end is None:
                code = f.read() + "\n"
            elif end is None:
                code = "".join(f.readlines()[start:]) + "\n"
            else:
                out = f.readlines()
                code = "".join(out[start:end])
                if len(out) < end:
                    code += "\n"

        element.children[0].children = code
        return super().render_fenced_code(element)

    def render_image(self, element):
        template = "![{}]({}{})"
        title = (
            ' "{}"'.format(element.title.replace('"', '\\"')) if element.title else ""
        )
        return template.format(self.render_children(element), element.dest, title)


_markdown = Markdown(renderer=MarkdownEmbCodeRenderer)


def convert(document: str):
    return _markdown(document)
