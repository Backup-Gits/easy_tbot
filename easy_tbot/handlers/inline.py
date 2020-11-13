from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import method_decorator
from abc import ABC, abstractmethod
# noinspection PyPackageRequirements
from telebot import types


class InlineHandler(HandlerSetup, ABC):
    """
    Base class for a inline handlers.
    """

    @abstractmethod
    def inline_filter(self, query: types.InlineQuery):
        """
       Filter a query and return true if this pass the test or false if not
       :param query: Query to filter
       :return: True or false
        """
        pass

    @abstractmethod
    def inline(self, query: types.InlineQuery):
        """
        Handle some incoming query.
        :param query: Query to handle.
        :return: None
        """
        pass

    def setup(self):
        self.bot.inline_handler(method_decorator(self.inline_filter))(method_decorator(method_decorator(self.inline)))
        super(InlineHandler, self).setup()
