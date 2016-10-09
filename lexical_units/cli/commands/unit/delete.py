from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.unit.unit import UnitCommand
from lexical_units.models import LexicalUnit


@command('delete', UnitCommand)
class DeleteCommand(Command, Utils):
    aliases = ('del',)

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')

    def action(self, args):
        unit_id = args.id
        q = LexicalUnit.objects.filter(id=unit_id)
        if q.count():
            unit = q.first()
            unit.delete()
            self.success_lexical_unit_deleted(unit_id)
        else:
            self.error_lexical_entry_not_found(unit_id)
