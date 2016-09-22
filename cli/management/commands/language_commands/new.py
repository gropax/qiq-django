from cli.management.commands._subcommand import Subcommand
from languages.models import Language


class NewCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='the iso-3 language code (ex: fra)')
        parser.add_argument('name', type=str, help='the name of the language')

    def execute(self, args, options):
        code = options['code']
        self.check_language_code_is_valid(code)
        self.check_language_does_not_exist(code)

        lang = Language(code=code, name=options['name'])
        lang.save()

        self.success_language_created(lang)
