from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.unit.unit import UnitCommand
from lexical_units.models import LexicalUnit
import termblocks as tb
import lexical_units.utils as lex
import core.cli.format as f


@command('info', UnitCommand)
class InfoCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')

    def action(self, args):
        unit_id = args.id

        q = LexicalUnit.objects.filter(id=unit_id)
        if not q.count():
            self.error_lexical_entry_not_found(unit_id)

        unit = q.first()

        lang = unit.language.code
        self.cfg = self.config().get('languages').get(lang)

        output = self.format(unit)
        self.stdout.write(output)

    def format(self, unit):
        table = f.model_table([
            ['ID', unit.id],
            ['Username', unit.user.username],
            ['Language', f.format_language(unit.language)],
            ['Created', f.format_creation_date(unit)],
            ['Lemma', unit.lemma],
            ['Patterns', unit.patterns.count()],
        ])

        text = tb.ColorTextBlock(self.format_colored(unit.patterns.all()))
        vlayout = tb.VerticalLayout([table, text])
        #margin = tb.MarginBlock(text, left=4, right=4, top=1, bottom=1)
        #vlayout = tb.VerticalLayout([table, margin])

        return vlayout.format()

    def format_colored(self, patterns):
        pats = [lex.parse_pattern(p.description) for p in patterns]
        colored = pats[0].format_termblock(self.cfg)
        for p in pats[1:]:
            colored.append({'text': '\n'})
            colored += p.format_termblock(self.cfg)
        return colored
