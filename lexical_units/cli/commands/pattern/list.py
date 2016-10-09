from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.pattern.pattern import PatternCommand
from lexical_units.models import LexicalPattern
import lexical_units.utils as lex
import cli.format as f


@command('list', PatternCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('language', type=str, help='the iso-3 of the language')

    def action(self, args):
        lang = args.language
        self.check_language_code_is_valid(lang)
        self.check_language_exists(lang)

        self.cfg = self.config().get('languages').get(lang, {})

        pats = LexicalPattern.objects.filter(lexical_unit__language=lang) \
                                     .order_by('lexical_unit__lemma')

        if not pats.all():
            self.error_no_match()

        output = self.format(pats)
        self.stdout.write(output)

    def format(self, pats):
        headers = ['ID', 'Lang', 'Lemma', 'Pattern']
        table = f.list_table(headers, pats, self.list_row_data)
        return table.format()

    def list_row_data(self, pat):
        return [
            pat.id,
            pat.lexical_unit.language.code,
            pat.lexical_unit.lemma,
            lex.parse_pattern(pat.description).format_termblock(self.cfg),
        ]
