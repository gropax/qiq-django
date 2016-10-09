from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.document import DocumentCommand
from notes.models import Document
import termblocks as tb
import core.cli.format as f


@command('list', DocumentCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        pass

    def action(self, args):
        docs = Document.objects.filter(user_id=1).all()

        if not docs.all():
            self.error_no_match()

        sort = sorted(docs, key=lambda d: d.name)

        output = self.format(sort)
        self.stdout.write(output)

    def format(self, docs):
        headers = ['ID', 'Project', 'Name', 'NoteID', 'Title']
        table = f.list_table(headers, docs, self.list_row_data)
        return table.format()

    def list_row_data(self, doc):
        return [
            doc.id,
            f.format_project_name(doc.note.project),
            doc.name,
            doc.note.id,
            f.format_document_title(doc),
        ]
