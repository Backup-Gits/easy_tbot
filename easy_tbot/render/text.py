from easy_tbot.loader import load_jinja_env


def render(template: str, context: dict) -> str:
    return load_jinja_env().get_template(template).render(**context)
