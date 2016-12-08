from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.pattern.pattern import PatternCommand
from lexical_units.models import LexicalPattern
import termblocks as tb
import lexical_units.utils as lex
import core.cli.format as f


@command('info', PatternCommand)
class InfoCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical pattern')

    def action(self, args):
        pat_id = args.id

        q = LexicalPattern.objects.filter(id=pat_id)
        if not q.count():
            self.error_lexical_pattern_not_found(pat_id)

        pat = q.first()

        lang = pat.lexical_unit.language.code
        self.cfg = self.config().get('languages').get(lang)

        output = self.format(pat)
        self.stdout.write(output)

    def format(self, pat):
        table = f.model_table([
            ['ID', pat.id],
            ['Username', pat.lexical_unit.user.username],
            ['Language', f.format_language(pat.lexical_unit.language)],
            ['Lemma', pat.lexical_unit.lemma],
            ['Created', f.format_date(pat)],
            ['Pattern', lex.parse_pattern(pat.description).format_termblock(self.cfg)],
        ])
        return table.format()
