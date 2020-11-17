from marko import Markdown
from marko.md_renderer import MarkdownRenderer


class MarkdownEmbEodeRenderer(MarkdownRenderer):
    def render_fenced_code(self, element):
        lang = element.__dict__.get("lang")
        lang, *file = lang.rsplit(":", 1)
        if len(file) == 1:
            with open(file[0], "r") as f:
                code = f.read()
            element.children[0].children = f"{code}\n"
        return super().render_fenced_code(element)

    def render_image(self, element):
        template = "![{}]({}{})"
        title = (
            ' "{}"'.format(element.title.replace('"', '\\"')) if element.title else ""
        )
        return template.format(self.render_children(element), element.dest, title)


def get_code_emb():
    markdown = Markdown(renderer=MarkdownEmbEodeRenderer)
    return markdown
