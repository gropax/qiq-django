from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalUnit


class DeleteCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')

    def execute(self, args, options):
        unit_id = options['id']
        q = LexicalUnit.objects.filter(id=unit_id)
        if q.count():
            unit = q.first()
            unit.delete()
            self.success_lexical_unit_deleted(unit_id)
        else:
            self.error_lexical_entry_not_found(unit_id)
