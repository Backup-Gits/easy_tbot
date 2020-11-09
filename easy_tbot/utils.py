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


class method_decorator(object):

    def __init__(self, func, obj=None, cls=None, method_type='function'):
        # These defaults are OK for plain functions
        # and will be changed by __get__() for methods once a method is dot-referenced.
        self.func, self.obj, self.cls, self.method_type = func, obj, cls, method_type

    def __get__(self, obj=None, cls=None):
        # It is executed when decorated func is referenced as a method: cls.func or obj.func.

        if self.obj == obj and self.cls == cls:
            return self  # Use the same instance that is already processed by previous call to this __get__().

        method_type = (
            'staticmethod' if isinstance(self.func, staticmethod) else
            'classmethod' if isinstance(self.func, classmethod) else
            'instancemethod'
            # No branch for plain function - correct method_type for it is already set in __init__() defaults.
        )

        return object.__getattribute__(self, '__class__')(
            # Use specialized method_decorator (or descendant) instance, don't change current instance attributes -
            # it leads to conflicts.
            self.func.__get__(obj, cls), obj, cls,
            method_type)  # Use bound or unbound method with this underlying func.

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __getattribute__(self, attr_name):  # Hiding traces of decoration.
        if attr_name in ('__init__', '__get__', '__call__', '__getattribute__', 'func', 'obj', 'cls',
                         'method_type'):  # Our known names. '__class__' is not included because is used only with
            # explicit object.__getattribute__().
            return object.__getattribute__(self, attr_name)  # Stopping recursion.
        # All other attr_names, including auto-defined by system in self, are searched in decorated self.func,
        # e.g.: __module__, __class__, __name__, __doc__, im_*, func_*, etc.
        return getattr(self.func,
                       attr_name)  # Raises correct AttributeError if name is not found in decorated self.func.

    def __repr__(self):  # Special case: __repr__ ignores __getattribute__.
        return self.func.__repr__()


class with_triggers(method_decorator):
    """
    Create a pre and post invocation trigger for a function
    """

    def __init__(self, func):
        super(with_triggers, self).__init__(func)

        self.__post_func: Callable = None

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
        results = super(with_triggers, self).__call__(*args, **kwargs)
        if self.__post_func is not None:
            self.__post_func(*args, **kwargs)
        return results
