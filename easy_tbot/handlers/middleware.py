from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import method_decorator
from abc import ABC, abstractmethod
from easy_tbot.bot.bot import Bot
# noinspection PyPackageRequirements
from telebot import types
from enum import Enum
import typing


class UpdateType(Enum):
    MESSAGE = 'message'
    EDITED_MESSAGE = 'edited_message'
    CHANNEL_POST = 'channel_post'
    EDITED_CHANNEL_POST = 'edited_channel_post'
    INLINE_QUERY = 'inline_query'
    CHOSEN_INLINE_RESULT = 'chosen_inline_result'
    CALLBACK_QUERY = 'callback_query'
    SHIPPING_QUERY = 'shipping_query'
    PRE_CHECKOUT_QUERY = 'pre_checkout_query'
    POLL = 'poll'


class Middleware(HandlerSetup, ABC):
    """
    Base class for a middleware. This manage and add needed info
    """
    update_types: typing.List[UpdateType] = [UpdateType.MESSAGE]

    @abstractmethod
    def middleware(self, bot: Bot, msg: types.Message):
        """
        Add, modify or delete a message info before any handler get it
        :param bot: The bot handling all the stuff
        :param msg: The message to modify
        """
        pass

    def setup(self):
        self.bot.middleware_handler(update_types=[ut.value for ut in self.update_types])(
            method_decorator(self.middleware))
        super(Middleware, self).setup()
