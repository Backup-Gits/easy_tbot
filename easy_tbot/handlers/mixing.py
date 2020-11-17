from .handler import HandlerSetup


class MixingException(Exception):
    pass


class Mixing(HandlerSetup):
    """
    This class must be first inheritance in a handler class mixing
    """

    def __init__(self, bot):
        super().__init__(bot)
        mro = self.__class__.__mro__
        if self.__class__ == Mixing:
            raise MixingException("This class can't be instantiated directly")
        elif len(mro) < 3:
            raise MixingException('Mixing class must be follow by classes to mix')
        elif mro[1] != Mixing:
            raise MixingException('Mixing class must be first in inheritance declaration')

    def setup(self):
        for cls in self.__class__.__mro__[2:]:
            if issubclass(cls, HandlerSetup):
                kwargs = {}
                if hasattr(cls, '_get_setup_kwargs_'):
                    kwargs = getattr(cls, '_get_setup_kwargs_')(self)
                # noinspection PyBroadException
                try:
                    getattr(cls, 'setup')(self, **kwargs)
                except Exception:
                    pass
