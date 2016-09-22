from cli.management.commands._subcommand import Subcommand
from languages.models import Language
import cli.format as f


class ListCommand(Subcommand):
    def add_arguments(self, parser):
        pass

    def execute(self, args, options):
        langs = Language.objects.all()

        if not langs.all():
            self.error_no_match()

        sort = sorted(langs, key=lambda l: l.code)

        output = self.format(sort)
        self.cmd.stdout.write(output)

    def format(self, langs):
        headers = ['Code', 'Name']
        table = f.list_table(headers, langs, self.list_row_data)
        return table.format()

    def list_row_data(self, lang):
        return [
            lang.code,
            lang.name,
        ]
