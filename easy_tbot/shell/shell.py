import argparse
from abc import ABC, abstractmethod


class ShellCommand(ABC):
    """
    Represents a command used in the OS shell
    """
    name: str
    extra: dict

    @abstractmethod
    def do(self, *args, **kwargs):
        """
        What does this the command do
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def __eq__(self, other):
        return other.name == self.name

    def post_insert(self, *args, **kwargs):
        """
        This method is invoked after the command is inserted in a shell handler
        :param args:
        :param kwargs:
        :return:None
        """
        pass


class ShellHandler:
    """
    Handles all commands and stuff of every base or created section in the bot
    """

    def __init__(self):
        self.__argparser = argparse.ArgumentParser()
        self.__subparser = self.__argparser.add_subparsers()
        self.__parsers = []
        self._subscriptions = []

    def add_command(self, command: ShellCommand):
        """
        Adds a command to the handler
        :param command: Command to add
        :return: None
        """
        if type(command) not in self._subscriptions:
            self._subscriptions.append(type(command))

        parser = self.__subparser.add_parser(command.name, **command.extra)
        parser.set_defaults(func=command.do)
        self.__parsers.append(parser)
        command.post_insert(parser)

    def add_commands(self, *args):
        """
        Adds a command  set to the handler
        :param args:
        :return:
        """
        for command in args:
            self.add_command(command)

    def process(self, *args):
        """
        Process the OS command input
        :param args:
        :return:
        """
        args = vars(self.__argparser.parse_args(args))
        if 'func' in args:
            func = args['func']
            del args['func']
            return func(**args)
        else:
            return self.__argparser.format_help()
