from core.cli.command import Command, command
from notes.cli.utils import Utils, NOTE_ATTRIBUTES
from notes.cli.commands.note import NoteCommand


@command('get', NoteCommand)
class GetCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('field', type=str, choices=NOTE_ATTRIBUTES,
                            help='the field to return')
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args):
        note = self.find_note_by_id_or_error(args.id)

        out = self.get_note_attribute(note, args.field)
        self.stdout.write(out)
