from notes.models import Note
from .base import NoteCommand


FIELDS = ['text']

class GetCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('field', type=str, choices=FIELDS, help='the field to return')
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        note = self.find_note_by_id_or_error(options['id'])

        if options['field'] == 'text':
            out = note.text

        self.cmd.stdout.write(out)