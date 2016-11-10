from core.cli.command import Command, command
from notes.cli.utils import Utils, NOTE_ATTRIBUTES
from notes.cli.commands.document import DocumentCommand


@command('get', DocumentCommand)
class GetCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('field', type=str, choices=NOTE_ATTRIBUTES,
                            help='the field to return')
        parser.add_argument('name_or_id', type=str, help='the name or ID of the document')

    def execute(self, args):
        doc = self.find_document_by_name_or_id_or_error(args.name_or_id)

        out = self.get_note_attribute(doc.note, args.field)
        self.stdout.write(out)
