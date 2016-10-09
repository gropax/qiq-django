from core.cli.command import Command, command
from languages.cli.utils import Utils
from languages.cli.commands.language import LanguageCommand
from languages.models import Language


@command('new', LanguageCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='the iso-3 language code (ex: fra)')
        parser.add_argument('name', type=str, help='the name of the language')

    def action(self, args):
        code = args.code
        self.check_language_code_is_valid(code)
        self.check_language_does_not_exist(code)

        lang = Language(code=code, name=args.name)
        lang.save()

        self.success_language_created(lang)
