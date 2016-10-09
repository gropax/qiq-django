from core.cli.command import Command, command
from core.cli.commands import QiqCommand


@command('note', QiqCommand)
class NoteCommand(Command):
    def action(self, args):
        self.parser.print_help()
