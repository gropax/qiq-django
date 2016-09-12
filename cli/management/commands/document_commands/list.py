from termblocks import TableBlock
from notes.models import Document
from .base import DocumentCommand
from cli.format import list_table, format_project_name, format_document_title


class ListCommand(DocumentCommand):
    def add_arguments(self, parser):
        pass

    def execute(self, args, options):
        docs = Document.objects.filter(user_id=1).all()

        if not docs.all():
            self.error_no_match()

        sort = sorted(docs, key=lambda d: d.name)

        output = self.format(sort)
        self.cmd.stdout.write(output)

    def format(self, docs):
        headers = ['ID', 'Project', 'Name', 'NoteID', 'Title']
        table = list_table(headers, docs, self.list_row_data)
        return table.format()

    def list_row_data(self, doc):
        return [
            doc.id,
            format_project_name(doc.note.project),
            doc.name,
            doc.note.id,
            format_document_title(doc),
        ]
