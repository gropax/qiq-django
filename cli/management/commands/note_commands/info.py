from notes.models import Note
from termblocks import TextBlock, MarginBlock, VerticalLayout
from .base import NoteCommand


class InfoCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        note = self.find_note_by_id_or_error(options['id'])

        output = self.format(note)
        self.cmd.stdout.write(output)

    def format(self, note):
        table = self.model_table([
            ['ID', note.id],
            ['Username', note.user.username],
            ['Project', self.format_project_name(note.project)],
            ['Original', self.format_original(note)],
            ['Documents', self.format_document_list(note)],
            ['Created', self.format_creation_date(note)],
            ['Virtual tags', self.format_virtual_tags(note)],
            ['Previous notes', self.format_references(note.references)],
            ['Next notes', self.format_references(note.referencers)],
            ['Rank', note.rank],
        ])
        text = TextBlock(note.text)
        margin = MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = VerticalLayout([table, margin])

        return vlayout.format()
