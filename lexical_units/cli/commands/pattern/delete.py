from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.pattern.pattern import PatternCommand
from lexical_units.models import LexicalPattern


@command('delete', PatternCommand)
class DeleteCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical pattern')

    def action(self, args):
        pat_id = args.id
        q = LexicalPattern.objects.filter(id=pat_id)
        if q.count():
            pat = q.first()
            pat.delete()
            self.success_lexical_pattern_deleted(pat_id)
        else:
            self.error_lexical_pattern_not_found(pat_id)
