from .shell import ShellHandler, ShellCommand

from easy_tbot.bot.loader import load_bot
from easy_tbot.db.loader import migrate
from easy_tbot.loader import for_app_do, get_logger

from easy_tbot.utils import Cached

from importlib import import_module
from argparse import ArgumentParser
import inspect
import os


class RunShellCommand(ShellCommand):
    """
    Command that starts the bot
    """
    name = 'run'
    extra = {
        'help': 'Run bot'
    }

    def do(self, *args, **kwargs):
        try:
            bot = load_bot()
            bot.polling()
        except Exception as e:
            get_logger().critical(f'Bot load failed with {e}')

    def post_insert(self, parser):
        pass


class MigrateShellCommand(ShellCommand):
    """
    Command that migrates all models in the database
    """
    name = 'migrate'
    extra = {
        'help': 'Populate the data base with models'
    }

    def do(self, *args, **kwargs):
        return migrate()

    def post_insert(self, parser):
        pass


class CreateApp(ShellCommand):
    # noinspection SpellCheckingInspection
    name = 'createsection'
    extra = {
        'help': 'Create a well formed section directory'
    }

    # noinspection SpellCheckingInspection
    files_and_lines = [('__init__.py', """"""),
                       ('handlers.py', """from easy_tbot import Command, render, types"""),
                       ('inlines.py', """from easy_tbot import InlineHandler, render, types"""),
                       ('middlewares.py', """from easy_tbot import Middleware, Bot, types"""),
                       ('models.py', """from easy_tbot.db import Model
from easy_tbot.db import Column, Integer, String, Boolean, ForeignKey, relationship"""),
                       ('shells.py', """from easy_tbot import ShellCommand""")]

    def do(self, *args, **kwargs):
        section = None
        if len(args) == 1:
            section = args[0]
        elif 'name' in kwargs:
            section = kwargs['name']
        full_section_name = os.path.join(os.getcwd(), section)
        if os.path.exists(full_section_name):
            return 'A folder with this name already exists'
        elif section is not None:
            os.mkdir(full_section_name)
            for fal in self.files_and_lines:
                file = fal[0]
                lines = fal[1]
                with open(os.path.join(full_section_name, file), 'w') as fs:
                    fs.write(lines)

    def post_insert(self, parser: ArgumentParser):
        parser.add_argument('name', help='Name for the section folder')


@Cached
def load_shell():
    """
    Loads and returns a ShellHandler with all shell commands in the bot project
    :return: ShellHandler
    """
    shell = ShellHandler()
    shell.add_commands(MigrateShellCommand(), RunShellCommand(), CreateApp())

    def handle_app(app):
        module = import_module(f'{app}.shells')
        for command in inspect.getmembers(module, inspect.isclass):
            if issubclass(command[1], ShellCommand) and \
                    not inspect.isabstract(command[1]) and \
                    command[1] is not ShellCommand:
                shell.add_command(command[1]())

    for_app_do(handle_app)
    return shell


def handle_shell_input(*args):
    data = load_shell().process(*args)
    if data is not None:
        print(data)
