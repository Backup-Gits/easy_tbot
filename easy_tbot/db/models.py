from .loader import get_model, get_session_class
from contextlib import contextmanager

Model = get_model()
Session = get_session_class()


@contextmanager
def session_scope():
    """
    A context for sections, for propely managemeent of our section.
    Example: with session_scope() as s: ...
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
