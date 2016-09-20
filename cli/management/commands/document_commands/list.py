from cli.management.commands._subcommand import Subcommand
from notes.models import Document
import termblocks as tb
import cli.format as f


class ListCommand(Subcommand):
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
