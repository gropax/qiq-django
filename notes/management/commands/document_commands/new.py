from .base import DocumentCommand


class NewCommand(DocumentCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the document (computer friendly)')
        parser.add_argument('note_id', type=int,
                            help='the id of the note representing the document')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the document')

    def execute(self, args, options):
        name = options['name']
        self.check_document_name_is_valid(name)
        self.check_document_name_does_not_exist(name)

        note = self.find_note_or_error(options['note_id'])
        self.check_note_is_original(note)

        desc = options['description']

        doc = self.create_document(name, note, desc)  # @fixme move method to helprs
        self.success_document_created(doc)
