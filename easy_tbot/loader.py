from importlib import import_module
import logging
import os
from typing import Callable
from .utils import Cached


@Cached
def load_settings():
    """
    Get the settings of the bot app
    :return: settings module
    """
    return import_module(os.environ.get('BOT_SETTING_MODULE'))


@Cached
def get_logger():
    """
    Get a logger for the framework
    :return: logger
    """
    logger = logging.getLogger('BOT')
    if load_settings().DEBUG:
        logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%('
                           'message)s"')
    ch.setFormatter(fm)
    logger.addHandler(ch)
    return logger


def for_app_do(func: Callable):
    """
    A helpfull method that iterate for every app and aply a function to them
    :param func: Funtion to aply
    :return: None
    """
    settings = load_settings()
    apps = set(settings.SECTIONS)

    for app in apps:
        try:
            return func(app)
        except ImportError as e:
            get_logger().warn(f"Failed to load: {e}")
        except Exception as e:
            get_logger().error(f'Exeption {e}')
