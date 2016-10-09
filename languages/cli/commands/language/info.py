from core.cli.command import Command, command
from languages.cli.utils import Utils
from languages.cli.commands.language import LanguageCommand


@command('info', LanguageCommand)
class InfoCommand(Command, Utils):
    def add_arguments(self, parser):
        pass

    def action(self, args):
        self.not_implemented()
