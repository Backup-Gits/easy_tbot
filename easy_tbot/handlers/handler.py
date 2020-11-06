from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from abc import ABC, abstractmethod

from telebot.types import Message
import typing


class BaseHandler(HandlerSetup, ABC):
    """
    Base class for a basic handlers.
    """
    @abstractmethod
    def handle(self, msg: Message):
        """
        Handles some incoming message.
        :param msg: Message to handle.
        :return: None
        """
        pass


class All(BaseHandler, ABC):
    """
    Handles all incoming mesagges
    """
    def setup(self):
        self.bot.message_handler(func=lambda x: True)(self.handle)
        super(All, self).setup()


class Command(BaseHandler, ABC):
    """
     Handles incoming mesagges asociated with a set of commands
     """
    commands: typing.List[str]

    def setup(self):
        self.bot.message_handler(commands=self.commands)(self.handle)
        super(Command, self).setup()


class Regex(BaseHandler, ABC):
    """
     Handles incoming mesagges asociated with a regular expresion
     """
    regex: str

    def setup(self):
        self.bot.message_handler(regexp=self.regex)(self.handle)
        super(Regex, self).setup()


class Function(BaseHandler, ABC):
    """
     Handles all incoming mesagges that pass through a filter function
     """
    @abstractmethod
    def filter(self, msg: Message) -> bool:
        """
        Filters a message and returns true if it has passed the test or false if it has not
        :param msg: Message to filter
        :return: True or false
        """
        pass

    def setup(self):
        self.bot.message_handler(func=self.filter)(self.handle)
        super(Function, self).setup()
