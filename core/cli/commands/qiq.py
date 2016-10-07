from core.cli.command import Command, command


@command('qiq')
class QiqCommand(Command):
    def add_arguments(self, parser):
        parser.add_argument('-f', type=str, default='dur')

    def action(self, args):
        print("+++ Qiq +++")
        print(args)
