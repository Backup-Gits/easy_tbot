from easy_tbot.handlers.setup.handlersetup import HandlerSetup
from easy_tbot.utils import Issolate
from abc import ABC, abstractmethod
from telebot import TeleBot
from telebot.types import Message
from enum import Enum
import typing


class UpdateType(Enum):
    MESSAGE = 'message'
    EDITED_MESSAGE = 'edited_message'
    CHANEL_POST = 'channel_post'
    EDITED_CHANEL_POST = 'edited_channel_post'
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
