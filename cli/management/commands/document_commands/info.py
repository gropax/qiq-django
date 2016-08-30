from notes.models import Note
from termblocks import TextBlock, MarginBlock, VerticalLayout
from .base import DocumentCommand


class InfoCommand(DocumentCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        output = self.format(doc)
        self.cmd.stdout.write(output)

    def format(self, doc):
        note = doc.note
        table = self.model_table([
            ['ID', doc.id],
            ['Username', note.user.username],
            ['Project', self.format_project_name(note.project)],
            ['Name', doc.name],
            ['Created', self.format_creation_date(doc)],
            ['Rank', note.rank],
        ])
        text = TextBlock(note.text)
        margin = MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = VerticalLayout([table, margin])

        return vlayout.format()
