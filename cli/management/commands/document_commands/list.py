from termblocks import TableBlock
from notes.models import Document
from .base import DocumentCommand


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

    #def format(self, docs):
        #headers = ['ID', 'Project', 'Name', 'NoteID', 'Title']
        #lines = [headers]
        #for doc in docs:
            #id = doc.id
            #proj = doc.note.project
            #proj_name = proj.full_name() if proj else '-'
            #name = doc.name
            #note_id = doc.note.id
            #desc = doc.description or '-'
            #lines.append([id, proj_name, name, note_id, desc])

        #table = TableBlock(lines, headers=['bold', 'underline'],
                           #color_line='grey', max_line=1)

        #return table.format()

    def format(self, docs):
        headers = ['ID', 'Project', 'Name', 'NoteID', 'Title']
        table = self.list_table(headers, docs, self.list_row_data)
        return table.format()

    def list_row_data(self, doc):
        return [
            doc.id,
            self.format_project_name(doc.note.project),
            doc.name,
            doc.note.id,
            self.format_document_title(doc),
        ]
