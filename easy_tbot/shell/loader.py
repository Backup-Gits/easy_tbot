from .shell import ShellHandler, ShellCommand

from easy_tbot.bot.loader import load_bot
from easy_tbot.db.loader import migrate
from easy_tbot.loader import for_app_do, get_logger

from easy_tbot.utils import Cached

from importlib import import_module
import inspect


class RunShellCommand(ShellCommand):
    """
    Command that start the bot
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
    Command that migrate all models in the database
    """
    name = 'migrate'
    extra = {
        'help': 'Populate the data base with models'
    }

    def do(self, *args, **kwargs):
        return migrate()

    def post_insert(self, parser):
        pass


@Cached
def load_shell():
    """
    Load a return a ShellHandler with all shell commands in the bot project
    :return: ShellHandler
    """
    shell = ShellHandler()
    shell.add_command.post_func = lambda c: get_logger().info(f'Successfully created {c.name} command')
    shell.add_commands(MigrateShellCommand(), RunShellCommand())

    def handle_app(app):
        module = import_module(f'{app}.shells')
        for command in inspect.getmembers(module, inspect.isclass):
            if issubclass(command[1], ShellCommand) and \
                    not inspect.isabstract(command[1]) and \
                    command[1] is not ShellCommand:
                shell.add_command(command[1])

    for_app_do(handle_app)
    return shell


def handle_shell_input(*args):
    data = load_shell().process(*args)
    if data is not None:
        print(data)
