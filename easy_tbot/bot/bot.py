# noinspection PyPackageRequirements
from telebot import TeleBot
from easy_tbot.handlers.setup import handlersetup
# noinspection PyPackageRequirements
from telebot import apihelper, logger
import logging
from easy_tbot.handlers.mixing import Mixing


class MetaSingleton(type):
    __instances__ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls.__instances__[cls]


class Bot(TeleBot, metaclass=MetaSingleton):
    """
    API's main class. Representation of a Telegram's bot.
    """

    def __init__(self, *args, **kwargs):
        """
        :param args: Must have at least a token.
        :param kwargs:
        """
        debug = False
        if 'debug' in kwargs:
            debug = kwargs['debug']
            del kwargs['debug']
        apihelper.ENABLE_MIDDLEWARE = True
        super(Bot, self).__init__(*args, **kwargs)

        if debug:
            logger.setLevel(logging.DEBUG)
        self.__subscriptions = []

    @property
    def proxy(self):
        """
        Gets the proxy info.
        :return: dict{'kind':'url'} where kind can be http or https or socks.
        """
        return apihelper.proxy

    @proxy.setter
    def proxy(self, value):
        """
        Sets the proxy info.
        :param value: Proxy in format dict{'kind':'url'} where kind can be http or https or socks.
        """
        apihelper.proxy = value

    def subscribe(self, k):
        """
        Subscribes a class k as a handler or middleware in the bot.
        :param k: Any handler class that extends of 'easy_tbot.handlers.setup.handlersetup.HandlerSetup'.
        :return: Instance of k class.
        """
        if not issubclass(k, handlersetup.HandlerSetup):
            raise ValueError(f'{k.__name__} is not a HandlerSetup child')
        if not issubclass(k, Mixing):
            for x in self.__subscriptions:
                if type(x) == k:
                    return x
        instance = k(self)
        self.__subscriptions.append(instance)
        return instance

    def subscribe_all(self, *args):
        """
        Subscribes a tuple of class as a handler or middleware in the bot.
        :param args: Tuple of any handler class that extends of 'easy_tbot.handlers.setup.handlersetup.HandlerSetup'.
        :return: A generator of instantiated subscriptions of args.
        """
        return [self.subscribe(x) for x in args]

    def setup(self):
        """
        Sets every class loaded in the bot, this is the real magic.
        :return: None.
        """
        for x in self.__subscriptions:
            x.setup()
