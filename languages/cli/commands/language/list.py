from core.cli.command import Command, command
from languages.cli.utils import Utils
from languages.cli.commands.language import LanguageCommand
from languages.models import Language
import core.cli.format as f


@command('list', LanguageCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        pass

    def action(self, args):
        langs = Language.objects.all()

        if not langs.all():
            self.error_no_match()

        sort = sorted(langs, key=lambda l: l.code)

        output = self.format(sort)
        self.stdout.write(output)

    def format(self, langs):
        headers = ['Code', 'Name']
        table = f.list_table(headers, langs, self.list_row_data)
        return table.format()

    def list_row_data(self, lang):
        return [
            lang.code,
            lang.name,
        ]
