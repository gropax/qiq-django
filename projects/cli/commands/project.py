from core.cli.command import Command, command
from core.cli.commands import QiqCommand


@command('project', QiqCommand)
class ProjectCommand(Command):
    aliases = ('proj',)

    def action(self, args):
        self.parser.print_help()
