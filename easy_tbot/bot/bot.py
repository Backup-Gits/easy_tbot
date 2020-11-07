from telebot import TeleBot
from easy_tbot.handlers.setup import handlersetup
from easy_tbot.utils import with_triggers
from telebot import apihelper, logger
import logging


class Bot(TeleBot):
    """
    Main class of api. Representation of a Telegram bot.
    """
    def __init__(self, *args, **kwargs):
        """
        :param args: Must have at least a token.
        :param kwargs:
        """
        debug = False
        if 'debug' in kwargs and kwargs['debug']:
            debug = kwargs['debug']
            del kwargs['debug']

        super(Bot, self).__init__(*args, **kwargs)
        if debug:
            logger.setLevel(logging.DEBUG)
        self.__subscriptions = []

    @property
    def proxy(self):
        """
        Get the proxy info.
        :return: dict{'kind':'url'} where kind can be http or https or socks.
        """
        return apihelper.proxy

    @proxy.setter
    def proxy(self, value):
        """
        Set the proxy info.
        :param value: Proxy in format dict{'kind':'url'} where kind can be http or https or socks.
        """
        apihelper.proxy = value

    @with_triggers
    def subscribe(self, k):
        """
        Subscribe a class k as a handler or middleware in the bot.
        :param k: Any handler class that extend of 'easy_tbot.handlers.setup.handlersetup.HandlerSetup'.
        :return: Instance of k class.
        """
        if not issubclass(k, handlersetup.HandlerSetup):
            raise ValueError(f'{k.__name__} is not a HandlerSetup child')
        instance = k(self)
        self.__subscriptions.append(instance)
        return instance

    def subscribe_all(self, *args):
        """
        Subscribe a tuple of class as a handler's or middleware's in the bot.
        :param args: Tuple of any handler class that extend of 'easy_tbot.handlers.setup.handlersetup.HandlerSetup'.
        :return: A generator of instantiated subscriptions of args.
        """
        for x in args:
            yield self.subscribe(x)

    @with_triggers
    def setup(self):
        """
        Setup every class loaded in the bot, this is the real magic.
        :return: None.
        """
        for x in self.__subscriptions:
            x.setup()
