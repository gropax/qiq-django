from core.cli.command import Command, command
from core.cli.commands import QiqCommand


@command('lexical', QiqCommand)
class LexicalCommand(Command):
    def action(self, args):
        self.parser.print_help()
