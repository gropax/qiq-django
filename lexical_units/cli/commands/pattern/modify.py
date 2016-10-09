from core.cli.command import Command, command
from lexical_units.cli.utils import Utils
from lexical_units.cli.commands.pattern.pattern import PatternCommand
from lexical_units.models import LexicalPattern


@command('modify', PatternCommand)
class ModifyCommand(Command, Utils):
    aliases = ('mod',)

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the id of the lexical unit')
        parser.add_argument('-d', '--description', type=str,
                            help='the new description of the lexical pattern')
        #parser.add_argument('-l', '--lemma', type=str,
                            #help='the new lemma of the lexical unit')


    def action(self, args):
        pat_id = args.id

        q = LexicalPattern.objects.filter(id=pat_id)
        if not q.count():
            self.error_lexical_pattern_not_found(pat_id)

        pat = q.first()

        new_desc = args.description
        if new_desc and new_desc != pat.description:
            pat.description = new_desc
            pat.save()
            self.success_lexical_pattern_modified(pat)
        else:
            self.warning_nothing_to_do()
