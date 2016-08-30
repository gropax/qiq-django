from django.core.management.base import BaseCommand, CommandParser, CommandError

from .document_commands.new import NewCommand
from .document_commands.info import InfoCommand
from .document_commands.list import ListCommand
from .document_commands.modify import ModifyCommand
from .document_commands.delete import DeleteCommand


def parser_class(cmd):
    """Hack function to allow subparsers"""
    class SubParser(CommandParser):
        def __init__(self, **kwargs):
            super(SubParser, self).__init__(cmd, **kwargs)
    return SubParser


SUBCOMMANDS = {
    'new': NewCommand,
    'info': InfoCommand,
    'list': ListCommand,
    'delete': DeleteCommand,
    'modify': ModifyCommand,
}
class Command(BaseCommand):
    help = 'Manage documents'

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
