from easy_tbot.loader import load_jinja_env


def render(template: str, **kwargs) -> str:
    """
    Format a text template using jinja
    """
    return load_jinja_env().get_template(template).render(**kwargs)
