import inspect
from importlib import import_module

from easy_tbot.utils import Cached
from easy_tbot.loader import load_settings, get_logger, for_app_do
from easy_tbot.handlers import middleware, handler, inline

from .bot import Bot

logger = get_logger()


class Loader:
    """
    A factory kind class, instances works as functions that load some base_class childs from a bot section
    """

    def __init__(self, base_class):
        self.__bc = base_class

    def __load(self, app):
        """
        Inner method, load classes from a section.
        :param app: Section for start loading.
        :return: Generator of class objects.
        """
        for load_class in inspect.getmembers(app, inspect.isclass):
            if issubclass(load_class[1], self.__bc) and load_class[1] is not self.__bc \
                    and not inspect.isabstract(load_class[1]):
                logger.info(f"{load_class[1].__name__} loaded")
                yield load_class[1]

    def __call__(self, app) -> list:
        """
        Load classes from a section.
        :param app: Section for start loading.
        :return: List of class objects.
        """
        return list(self.__load(app))


def easy_subscribe(module, cast_type, bot):
    """
    Subscribes in a bot the class of the passed module childs by inheritance of cast_type.
    :param module: Module to search for classes.
    :param cast_type: Base class of classes to search.
    :param bot: Bot for making subscriptions.
    :return: None.
    """
    lmodule = import_module(module)
    bot.subscribe_all(*Loader(cast_type)(lmodule))


@Cached
def load_bot() -> Bot:
    """
    Main class of loader package, load and return a well formed bot from project
    :return: Bot
    """
    settings = load_settings()
    bot: Bot = Bot(settings.TOKEN, debug=settings.DEBUG)
    if settings.PROXY is not None and len(settings.PROXY) > 0:
        bot.proxy = settings.PROXY
    get_logger().info('Successfully created bot')
    bot.subscribe.post_func = lambda k: get_logger().info(f' Successfully subscribed {k.__name__}')

    def handle_app(app):
        for name, cast_type in [('middlewares', middleware.Middleware), ('handlers', handler.BaseHandler),
                                ('inlines', inline.InlineHandler)]:
            try:
                easy_subscribe(f'{app}.{name}', cast_type, bot)
            except (ImportError, TypeError):
                logger.warn(f"Can't find {name} file in {app}")
    for_app_do(handle_app)
    bot.setup()
    return bot
