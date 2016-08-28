from notes.models import Note
from notes.helpers import virtual_tags
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from .base import NoteCommand


class InfoCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        note = self.find_note_by_id_or_error(options['id'])

        output = self.format_info(note)
        self.cmd.stdout.write(output)

    def format_info(self, note):
        id = note.id
        username = note.user.username
        proj = note.project
        project = proj.full_name() if proj else '-'
        docs = ", ".join(d.name for d in note.documents.all()) or '-'
        created = note.created.strftime("%Y-%m-%d %H:%M:%S") + " (%s)" % note.age() #self.note_age(note)
        vtags = " ".join(tag for tag in virtual_tags(note))
        prev = ",".join(str(n.id) for n in note.references.all()) or '-'
        next = ",".join(str(n.id) for n in note.referencers.all()) or '-'
        rank = note.rank

        table = TableBlock([
            ['Name', 'Value'],
            ['ID', id],
            ['Username', username],
            ['Project', project],
            ['Documents', docs],
            ['Created', created],
            ['Virtual tags', vtags],
            ['Previous notes', prev],
            ['Next notes', next],
            ['Rank', rank],
        ], headers=['bold', 'underline'], color_line='grey')

        text = TextBlock(note.text)
        margin = MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = VerticalLayout([table, margin])

        return vlayout.format()