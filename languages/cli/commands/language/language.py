from core.cli.command import Command, command
from core.cli.commands import QiqCommand


@command('language', QiqCommand)
class LanguageCommand(Command):
    aliases = ('lang',)

    def action(self, args):
        self.parser.print_help()
