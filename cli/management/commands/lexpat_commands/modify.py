from django.core.exceptions import ObjectDoesNotExist
from cli.management.commands._subcommand import Subcommand
from lexical_units.models import LexicalPattern
import cli.utils.projects as prj


class ModifyCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')
        parser.add_argument('-d', '--description', type=str,
                            help='the new description of the lexical pattern')
        #parser.add_argument('-l', '--lemma', type=str,
                            #help='the new lemma of the lexical unit')


    def execute(self, args, options):
        pat_id = options['id']

        q = LexicalPattern.objects.filter(id=pat_id)
        if not q.count():
            self.error_lexical_pattern_not_found(pat_id)

        pat = q.first()

        new_desc = options['description']
        if new_desc and new_desc != pat.description:
            pat.description = new_desc
            pat.save()
            self.success_lexical_pattern_modified(pat)
        else:
            self.warning_nothing_to_do()
