from django.core.exceptions import ObjectDoesNotExist
from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalUnit
import cli.utils.projects as prj


class ModifyCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')
        parser.add_argument('-l', '--lemma', type=str,
                            help='the new lemma of the lexical unit')

    def execute(self, args, options):
        unit_id = options['id']

        q = LexicalUnit.objects.filter(id=unit_id)
        if not q.count():
            self.error_lexical_entry_not_found(unit_id)

        unit = q.first()

        new_lemma = options['lemma']
        if new_lemma and new_lemma != unit.lemma:
            unit.lemma = new_lemma
            unit.save()
            self.success_lexical_unit_modified(unit)
        else:
            self.warning_nothing_to_do()
