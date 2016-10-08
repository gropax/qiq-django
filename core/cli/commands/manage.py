from core.cli.command import Command, command
from core.cli.commands.qiq import QiqCommand


@command('manage', QiqCommand)
class ManageCommand(Command):
    pass
