import os
from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.document import DocumentCommand


@command('new', DocumentCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the document (computer friendly)')
        parser.add_argument('note_id', type=int,
                            help='the id of the note representing the document')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the document')
        parser.add_argument('-f', '--file', type=str,
                            help='synchronize document with file')

    def action(self, args):
        name = args.name
        self.check_document_name_is_valid(name)
        self.check_document_name_does_not_exist(name)

        note = self.find_note_by_id_or_error(args.note_id)
        self.check_note_is_original(note)

        desc = args.description

        f = None
        if args.file:
            f = self.absolute_path(args.file)
            if os.path.isfile(f):
                if not self.ask('File `%s` already exists. Synchronize it anyway ?' % f, default='no'):
                    self.warning_operation_aborted()

        doc = self.create_document(name, note, desc, f)  # @fixme move method to helprs
        self.synchronize_document(doc)
        self.success_document_created(doc)
