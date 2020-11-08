from abc import ABC, abstractmethod
from telebot import TeleBot
from typing import Callable


class HandlerSetup(ABC):
    """
    Very base class, of anything that can be setup in a  bot, base class for every handler
    """

    def __init__(self, bot: TeleBot):
        """
        This method must be called in other class different than HandlerSetup and should be initialized on that class
        :param bot: Bot, telegram bot
        """
        self.__bot = bot
        self.__is_set_up = False

    @property
    def is_setup(self) -> bool:
        """
        Checks if a handler has been set inside a bot before
        :return: If handler has been set inside a bot before
        """
        return self.__is_set_up

    @property
    def bot(self) -> TeleBot:
        """
        Gets the bot using this handler
        :return: Bot, inner bot
        """
        return self.__bot

    @property
    @abstractmethod
    def _issolated_function_(self) -> Callable:
        """
        Issolate the inner function for decoration purpose
        """
        pass

    def setup(self):
        """
        Sets this handler in the proper bot
        :return: None
        """
        self.__is_set_up = True
