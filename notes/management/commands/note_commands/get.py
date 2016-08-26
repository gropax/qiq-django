from notes.models import Note
from .base import NoteCommand


FIELDS = ['text']

class GetCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('field', type=str, choices=FIELDS, help='the field to return')
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        try:
            note = Note.objects.get(id=options['id'])
        except:
            self.notify_not_found(options['id'])
            exit(1)

        if options['field'] == 'text':
            out = note.text

        self.cmd.stdout.write(out)
