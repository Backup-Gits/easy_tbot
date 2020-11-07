from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from abc import ABC, abstractmethod
from telebot.types import InlineQuery


class InlineHandler(HandlerSetup, ABC):
    """
    Base class for a inline handlers.
    """
    @abstractmethod
    def filter(self, query: InlineQuery):
        """
       Filter a query and return trun if this pass the test or false if not
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
        self.bot.inline_handler(self.filter)(self.inline)
        super(InlineHandler, self).setup()
