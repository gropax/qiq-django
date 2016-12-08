from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.document import DocumentCommand
import termblocks as tb
import core.cli.format as f


@command('info', DocumentCommand)
class InfoCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')

    def action(self, args):
        name_or_id = args.name_or_id
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        self.synchronize_document(doc)

        output = self.format(doc)
        self.stdout.write(output)

    def format(self, doc):
        note = doc.note
        table = f.model_table([
            ['ID', doc.id],
            ['Username', note.user.username],
            ['Project', f.format_project_name(note.project)],
            ['Name', doc.name],
            ['File', doc.file],
            ['Created', f.format_date(doc.created)],
            ['Edited', f.format_date(doc.note.modified)],
            ['Rank', note.rank],
        ])
        text = tb.TextBlock(note.text)
        margin = tb.MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = tb.VerticalLayout([table, margin])

        return vlayout.format()
