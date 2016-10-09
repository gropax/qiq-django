from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand


FIELDS = ['text']

@command('get', NoteCommand)
class GetCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('field', type=str, choices=FIELDS, help='the field to return')
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args):
        note = self.find_note_by_id_or_error(args.id)

        if args.field == 'text':
            out = note.text

        self.stdout.write(out)
