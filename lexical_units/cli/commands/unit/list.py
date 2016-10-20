from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.unit.unit import UnitCommand
from languages.models import Language
from lexical_units.models import LexicalUnit
import core.cli.format as f


@command('list', UnitCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='the iso-3 of the language')

    def action(self, args):
        lang = args.language
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        units = LexicalUnit.objects.filter(user_id=1, language=lang).all()

        if not units.all():
            self.error_no_match()

        output = self.format(units)
        self.stdout.write(output)

    def format(self, units):
        headers = ['ID', 'Lang', 'Pat', 'Cat', 'Lemma', 'Definition']
        table = f.list_table(headers, units, self.list_row_data)
        return table.format()

    def list_row_data(self, unit):
        return [
            unit.id,
            unit.language.code,
            unit.patterns.count(),
            unit.grammatical_category,
            unit.lemma,
            unit.definition or '-',
        ]
