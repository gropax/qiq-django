from notes.models import Note
from termblocks import TextBlock, MarginBlock, VerticalLayout
from .base import NoteCommand
from cli.format import model_table, format_project_name, format_original, format_document_list, format_creation_date, format_references, format_virtual_tags


class InfoCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        note = self.find_note_by_id_or_error(options['id'])

        output = self.format(note)
        self.cmd.stdout.write(output)

    def format(self, note):
        table = model_table([
            ['ID', note.id],
            ['Username', note.user.username],
            ['Project', format_project_name(note.project)],
            ['Original', format_original(note)],
            ['Documents', format_document_list(note)],
            ['Created', format_creation_date(note)],
            ['Virtual tags', format_virtual_tags(note)],
            ['Previous notes', format_references(note.references)],
            ['Next notes', format_references(note.referencers)],
            ['Rank', note.rank],
        ])
        text = TextBlock(note.text)
        margin = MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = VerticalLayout([table, margin])

        return vlayout.format()
