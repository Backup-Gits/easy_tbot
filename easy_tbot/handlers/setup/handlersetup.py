from abc import ABC
from telebot import TeleBot


class HandlerSetup(ABC):
    """
    Very base class, of anything that can be setup in a  bot, base class for every handler
    """

    def __init__(self, bot: TeleBot):
        """
        This method must be called in other class than HandlerSetup, initialize that class
        :param bot: Bot, telegram bot
        """
        self.__bot = bot
        self.__is_set_up = False

    @property
    def is_setup(self) -> bool:
        """
        Get if  handler has being setup inside a bot
        :return: If  handler has being setup inside a bot
        """
        return self.__is_set_up

    @property
    def bot(self) -> TeleBot:
        """
        Get the bot using this handler
        :return: Bot, inner bot
        """
        return self.__bot

    def setup(self):
        """
        Setup this handler in the proper bot
        :return: None
        """
        self.__is_set_up = True
