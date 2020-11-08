from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import Issolate
from abc import ABC, abstractmethod
from telebot import TeleBot
from telebot.types import Message
from enum import Enum
import typing


class UpdateType(Enum):
    pass  # TODO: update this


class Middleware(HandlerSetup, ABC):
    """
    Base class for a middleware. This manage and add needed info
    """
    update_types: typing.List[UpdateType]

    @abstractmethod
    def middleware(self, bot: TeleBot, msg: Message):
        """
        Add, modify or delete a message info before any handler get it
        :param bot: The bot handling all the stuff
        :param msg: The message to modify
        """
        pass

    def setup(self):
        self.bot.middleware_handler(update_types=[ut.value for ut in self.update_types])(Issolate(self.middleware))
        super(Middleware, self).setup()
