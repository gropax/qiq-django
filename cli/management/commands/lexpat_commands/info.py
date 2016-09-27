from cli.management.commands._subcommand import Subcommand
import termblocks as tb
from lexical_units.models import LexicalPattern
import lexical_units.utils as lex
import cli.format as f


class InfoCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical pattern')

    def execute(self, args, options):
        pat_id = options['id']

        q = LexicalPattern.objects.filter(id=pat_id)
        if not q.count():
            self.error_lexical_pattern_not_found(pat_id)

        pat = q.first()

        lang = pat.lexical_unit.language.code
        self.cfg = self.config().get('languages').get(lang)

        output = self.format(pat)
        self.cmd.stdout.write(output)

    def format(self, pat):
        table = f.model_table([
            ['ID', pat.id],
            ['Username', pat.lexical_unit.user.username],
            ['Language', f.format_language(pat.lexical_unit.language)],
            ['Lemma', pat.lexical_unit.lemma],
            ['Created', f.format_creation_date(pat)],
            ['Pattern', lex.parse_pattern(pat.description).format_termblock(self.cfg)],
        ])
        return table.format()
