from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import method_decorator
from abc import ABC, abstractmethod
# noinspection PyPackageRequirements
from telebot import types
import typing


class BaseHandler(HandlerSetup, ABC):
    """
    Base class for a basic handlers.
    """

    @abstractmethod
    def handle(self, msg: types.Message):
        """
        Handles some incoming message.
        :param msg: Message to handle.
        :return: None
        """
        pass

    @abstractmethod
    def _get_setup_kwargs_(self) -> dict:
        pass

    def setup(self, *args, **kwargs):
        k_args = self._get_setup_kwargs_() if len(kwargs) == 0 or kwargs is None else kwargs
        self.bot.message_handler(**k_args)(method_decorator(self.handle))
        super(BaseHandler, self).setup()


class All(BaseHandler, ABC):
    """
    Handles all incoming messages
    """

    def _get_setup_kwargs_(self) -> dict:
        return {'func': lambda x: True}


class Command(BaseHandler, ABC):
    """
     Handles incoming messages associated with a set of commands
     """
    commands: typing.List[str]

    def _get_setup_kwargs_(self) -> dict:
        return {'commands': self.commands}


class Regex(BaseHandler, ABC):
    """
     Handles incoming messages associated with a regular expression
     """
    regex: str

    def _get_setup_kwargs_(self) -> dict:
        return {'regexp': self.regex}


class Function(BaseHandler, ABC):
    """
     Handles all incoming messages that pass through a filter function
     """

    @abstractmethod
    def filter(self, msg: types.Message) -> bool:
        """
        Filters a message and returns true if it has passed the test or false if it has not
        :param msg: Message to filter
        :return: True or false
        """
        pass

    def _get_setup_kwargs_(self) -> dict:
        return {'func': method_decorator(self.filter)}
