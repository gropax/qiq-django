from core.cli.command import Command, command
from languages.cli.utils import Utils
from languages.cli.commands.language import LanguageCommand


@command('modify', LanguageCommand)
class ModifyCommand(Command, Utils):
    aliases = ('mod',)

    def add_arguments(self, parser):
        pass

    def action(self, args):
        self.not_implemented()
