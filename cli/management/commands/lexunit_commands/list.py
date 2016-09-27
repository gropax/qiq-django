from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalUnit
import cli.format as f


class ListCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='the iso-3 of the language')

    def execute(self, args, options):
        lang = options['language']
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        units = LexicalUnit.objects.filter(user_id=1, language=lang).all()

        if not units.all():
            self.error_no_match()

        output = self.format(units)
        self.cmd.stdout.write(output)

    def format(self, units):
        #headers = ['ID', 'Lang', 'Cat', 'Lemma']
        headers = ['ID', 'Lang', 'Pat', 'Lemma']
        table = f.list_table(headers, units, self.list_row_data)
        return table.format()

    def list_row_data(self, unit):
        return [
            unit.id,
            unit.language.code,
            unit.patterns.count(),
            #unit.category,
            unit.lemma,
        ]
