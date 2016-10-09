from core.cli.command import Command, command
from lexical_units.cli.commands import LexicalCommand


@command('pattern', LexicalCommand)
class PatternCommand(Command):
    aliases = ('pat',)

    def action(self, args):
        self.parser.print_help()
