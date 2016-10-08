from core.cli.command import Command, command
from core.cli.commands.manage import ManageCommand


@command('fake', ManageCommand)
class FakeCommand(Command):
    def add_arguments(self, parser):
        parser.add_argument('test', type=str, default='bile')

    def action(self, args):
        self.stdout.write("+++ Fake +++\n")
        #print(args)
        #Project(user_id=1, name='bitocul').save()
