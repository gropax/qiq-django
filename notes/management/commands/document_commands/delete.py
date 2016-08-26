import sys
from notes.models import Document
from .base import DocumentCommand


class DeleteCommand(DocumentCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        doc.delete()
        self.success_document_deleted(doc)

    def success_document_deleted(self, doc):
        s = "Document `%s` deleted" % doc.name
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))
