from core.cli.command import Command, command
from core.cli.commands.qiq import QiqCommand


@command('manage', QiqCommand)
class ManageCommand(Command):
    def add_arguments(self, parser):
        pass
        #parser.add_argument('test', type=str, default='bile')

    def action(self, args):
        print("+++ Manage +++")
        print(args)
