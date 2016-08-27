from django.core.management.base import BaseCommand, CommandParser, CommandError
from notes.models import Note
from notes.helpers import merge_notes
from .base import NoteCommand


class MergeCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')
        #input_grp.add_argument('-e', '--editor', type=str,
                                #default='vim % -u NONE -c startinsert',
                                #help='the command used to open the editor')

        proj_grp = parser.add_mutually_exclusive_group()
        proj_grp.add_argument('-p', '--project', type=str,
                                help='the project in which to store the note')
        proj_grp.add_argument('-P', '--no-project', action='store_true', default=False,
                                help='do not store the note in any project')
        parser.add_argument('-c', '--create-project', action='store_true', default=False,
                                help='create the project if it doesn\'t exist')

    def execute(self, args, options):
        notes = self.filter_notes(options['filters']).all()

        if not notes:
            self.error_no_match()

        proj = self.get_or_prompt_project(options)

        text = "\n\n".join(note.text for note in notes)
        f = self.edit_note_in_editor(options, text=text)

        with open(f, 'r') as file:
            text = file.read()

        if text:
            note = merge_notes(proj, text, notes)
            self.success_note_created(note)
        else:
            exit(1)