from jinja2 import Environment, FileSystemLoader, select_autoescape
from importlib import import_module
from typing import Callable
from .utils import Cached
import logging
import os


@Cached
def load_settings():
    """
    Gets the settings of the bot app
    :return: settings module
    """
    return import_module(os.environ.get('BOT_SETTING_MODULE'))


@Cached
def get_logger():
    """
    Gets a logger for the framework
    :return: logger
    """
    settings = load_settings()

    logger = logging.getLogger(os.path.basename(settings.BASEDIR))
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.NOTSET)
    ch = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%('
                           'message)s"')
    ch.setFormatter(fm)
    logger.addHandler(ch)
    return logger


def for_app_do(func: Callable):
    """
    A helpful method that iterates for every app and applies a function to them
    :param func: Function to apply
    :return: None
    """
    settings = load_settings()

    for app in settings.SECTIONS:
        try:
            func(app)
        except ImportError as e:
            get_logger().warn(f"Failed to load: {e}")
        except Exception as e:
            get_logger().error(f'Exception {e}')


@Cached
def load_jinja_env():
    templates = load_settings().TEMPLATES
    loader = FileSystemLoader(templates['DIR'])
    auto_escape = select_autoescape(templates['AUTO_ESCAPE'])
    return Environment(loader=loader, autoescape=auto_escape)
