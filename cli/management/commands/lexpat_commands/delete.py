from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalPattern


class DeleteCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical pattern')

    def execute(self, args, options):
        pat_id = options['id']
        q = LexicalPattern.objects.filter(id=pat_id)
        if q.count():
            pat = q.first()
            pat.delete()
            self.success_lexical_pattern_deleted(pat_id)
        else:
            self.error_lexical_pattern_not_found(pat_id)
