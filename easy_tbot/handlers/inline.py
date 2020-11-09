from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import method_decorator
from abc import ABC, abstractmethod
from telebot.types import InlineQuery
from typing import Callable


class InlineHandler(HandlerSetup, ABC):
    """
    Base class for a inline handlers.
    """

    @abstractmethod
    def filter(self, query: InlineQuery):
        """
       Filter a query and return true if this pass the test or false if not
       :param query: Query to filter
       :return: True or false
        """
        pass

    @abstractmethod
    def inline(self, query):
        """
        Handle some incoming query.
        :param query: Query to handle.
        :return: None
        """
        pass

    def setup(self):
        self.bot.inline_handler(method_decorator(self.filter))(method_decorator(method_decorator(self.inline)))
        super(InlineHandler, self).setup()
