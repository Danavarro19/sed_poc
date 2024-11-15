from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("./view/templates"),
    autoescape=select_autoescape()
)


def render_template(template, context=None):
    template = env.get_template(template)
    if context:
        return template.render(**context)
    return template.render()
