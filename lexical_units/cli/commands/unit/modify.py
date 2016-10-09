from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.unit.unit import UnitCommand
from languages.models import Language
from lexical_units.models import LexicalUnit
from django.core.exceptions import ObjectDoesNotExist
from projects.cli import utils2 as prj


@command('modify', UnitCommand)
class ModifyCommand(Command, Utils):
    aliases = ('mod',)

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')
        parser.add_argument('-l', '--lemma', type=str,
                            help='the new lemma of the lexical unit')

    def action(self, args):
        unit_id = args.id

        q = LexicalUnit.objects.filter(id=unit_id)
        if not q.count():
            self.error_lexical_entry_not_found(unit_id)

        unit = q.first()

        new_lemma = args.lemma
        if new_lemma and new_lemma != unit.lemma:
            unit.lemma = new_lemma
            unit.save()
            self.success_lexical_unit_modified(unit)
        else:
            self.warning_nothing_to_do()
