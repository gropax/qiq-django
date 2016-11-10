from core.cli.command import Command, command
from core.cli.commands import QiqCommand


@command('document', QiqCommand)
class DocumentCommand(Command):
    aliases = ('doc',)

    def action(self, args):
        self.parser.print_help()
