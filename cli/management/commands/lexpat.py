from django.core.management.base import BaseCommand, CommandParser, CommandError
from .lexpat_commands.new import NewCommand
from .lexpat_commands.list import ListCommand
from .lexpat_commands.modify import ModifyCommand
from .lexpat_commands.delete import DeleteCommand
from .lexpat_commands.info import InfoCommand


def parser_class(cmd):
    """Hack function to allow subparsers"""
    class SubParser(CommandParser):
        def __init__(self, **kwargs):
            super(SubParser, self).__init__(cmd, **kwargs)
    return SubParser


SUBCOMMANDS = {
    'new': NewCommand,
    'list': ListCommand,
    'modify': ModifyCommand,
    'delete': DeleteCommand,
    'info': InfoCommand,
}
class Command(BaseCommand):
    help = 'Manage lexical units'

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
