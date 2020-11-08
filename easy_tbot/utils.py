from functools import lru_cache
from typing import Callable
import functools
from copy import copy


class Cached:
    """
    Decorator object, for cachin and some lazy initialization
    """

    def __init__(self, func):
        """
        :param func; Function to cach and make lazy
        """
        self.__func = func

    @lru_cache
    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


class Issolate(object):
    """
    Issolate a function class as a objetc for support of functions decorators
    """

    def __init__(self, func):
        """

        :param func: Function decorated, converted in a trigger holder
        """
        self.__self__ = None  # "__self__" is also used by bound methods

        self._wrapped_ = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        # if bound to an object, pass it as the first argument
        fixed_args = (self.__self__,) + args if self.__self__ is not None else args

        # == change the following line to make the decorator do something ==
        return self._wrapped_(*fixed_args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # create a bound copy
        bound = copy(self)
        bound.__self__ = instance

        # update __doc__ and similar attributes
        functools.update_wrapper(bound, self._wrapped_)

        # add the bound instance to the object's dict so that
        # __get__ won't be called a 2nd time
        setattr(instance, self._wrapped_.__name__, bound)

        return bound


class WithTriggers(Issolate):
    """
    Create a pre and post invocation trigger for a function
    """

    def __init__(self, func):
        super(WithTriggers, self).__init__(func)

        self.__pre_func: Callable = None
        self.__post_func: Callable = None

    @property
    def pre_func(self):
        """
        Get function that trigger before main invocation
        :return: Callable
        """
        return self.__pre_func

    @pre_func.setter
    def pre_func(self, value):
        """
        Set function that trigger before main invocation
        :param value:  Function that trigger before main invocation
        :return: None
        """
        self.__pre_func = value

    @property
    def post_func(self):
        """
        Get function that trigger after main invocation
        :return: Callable
        """
        return self.__post_func

    @post_func.setter
    def post_func(self, value):
        """
        Get function that trigger after main invocation
        :return: Callable
        """
        self.__post_func = value

    def __call__(self, *args, **kwargs):
        if self.__pre_func is not None:
            self.__pre_func(*args, **kwargs)
        results = super(WithTriggers, self).__call__(*args, **kwargs)
        if self.__post_func is not None:
            self.__post_func(*args, **kwargs)
        return results


def with_triggers(f):
    """Easy decorator, just a thing nice to see and code for PE8 conventions (non capitalized and other stuff)"""
    return WithTriggers(f)
