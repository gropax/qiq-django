from core.cli.command import Command, command
from core.cli.commands.manage import ManageCommand


@command('fake', ManageCommand)
class FakeCommand(Command):
    def add_arguments(self, parser):
        parser.add_argument('test', type=str, default='bile')

    def action(self, args):
        print("+++ Fake +++")
        print(args)
