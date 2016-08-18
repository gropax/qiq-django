from django.core.management.base import BaseCommand, CommandParser, CommandError
from notes.models import Note
from ._term_blocks import TableBlock
from ._notes_cmd import NoteCommand


class ListCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        q = self.filter_query(options['filters'])
        notes = Note.objects.filter(**q).all()
        output = self.format(notes)
        self.cmd.stdout.write(output)

    def format(self, notes):
        if not notes.all():
            self.notify_empty_set()

        headers = ['ID', 'Project', 'Rk', 'Text']
        lines = [headers]
        for note in notes:
            id = note.id
            proj = note.project
            project = proj.full_name() if proj else '-'
            rank = note.rank
            text = note.text
            #created = note.created
            lines.append([id, project, rank, text])

        table = TableBlock(lines, headers=['bold', 'underline'],
                           color_line='grey', max_line=1)

        return table.format()
