from django.core.management.base import BaseCommand, CommandParser, CommandError

from .subcommands.new import NewCommand
from .subcommands.info import InfoCommand
from .subcommands.delete import DeleteCommand
from .subcommands.list import ListCommand
from .subcommands.merge import MergeCommand
from .subcommands.get import GetCommand


def parser_class(cmd):
    """Hack function to allow subparsers"""
    class SubParser(CommandParser):
        def __init__(self, **kwargs):
            super(SubParser, self).__init__(cmd, **kwargs)
    return SubParser


SUBCOMMANDS = {
    'new': NewCommand,
    'info': InfoCommand,
    'delete': DeleteCommand,
    'list': ListCommand,
    'merge': MergeCommand,
    'get': GetCommand,
}
class Command(BaseCommand):
    help = 'Manage notes'

    def __init__(self, *args, **kwargs):
        self.subcmds = {cmd: klass(self) for cmd, klass in SUBCOMMANDS.items()}
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        cmd_parsers = parser.add_subparsers(help='@todo', dest='cmd',
                                            parser_class=parser_class(self))
        for cmd_str, cmd in self.subcmds.items():
            cmd_parser = cmd_parsers.add_parser(cmd_str)
            cmd.add_arguments(cmd_parser)
        self.parser = parser

    def handle(self, *args, **options):
        cmd = options['cmd']
        if cmd:
            self.subcmds[cmd].execute(args, options)
        else:
            self.parser.print_help()
