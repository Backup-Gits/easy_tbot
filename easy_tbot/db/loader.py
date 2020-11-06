from easy_tbot.utils import Cached
from easy_tbot.loader import load_settings, for_app_do, get_logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from importlib import import_module
import inspect


@Cached
def load_dbengine():
    """
    Gets the database engine for the project.
    :return: Base (db engine class of sqlalchemy package).
    """
    settings = load_settings()
    return create_engine(settings.DB)


@Cached
def get_model():
    """
    Gets the declarative base for an ORM based on a Class System.
    :return: DeclarativeMeta.
    """
    return declarative_base()


@Cached
def get_session_class():
    """
    Constructs a new class type for defining sessions in the data base engine.
    :return: New class for definig sessions.
    """
    return sessionmaker(load_dbengine())


def migrate():
    """
    Write the proper tables in the database, sometimes it generates a database (sqlite).
    :return: All subcriptions models of the database, the datatables in raw format.
    """
    subcriptions = []
    model = get_model()

    def handle_app(app):
        app_module = import_module(f'{app}.models')
        for table in inspect.getmembers(app_module, inspect.isclass):
            if issubclass(table[1], model) and table[1] is not model:
                subcriptions.append(table[1].__table__)
                get_logger().info(f'Successfully analyzed {table[0]}')

    for_app_do(handle_app)

    model.metadata.create_all(load_dbengine(), tables=subcriptions)
    return subcriptions
