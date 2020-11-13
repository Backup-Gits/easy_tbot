from .handler import HandlerSetup
import inspect


class Mixing(HandlerSetup):
    """
    This class must be first inheritance in a handler class mixing
    """
    def setup(self):
        for cls in self.__class__.__mro__[2:]:
            if hasattr(cls, 'setup') and not inspect.isabstract(cls):
                getattr(cls, 'setup')(self)
