from django.core.management.base import BaseCommand, CommandParser, CommandError
import re
#from termcolor import colored
from notes.models import Note
from termblocks import TableBlock
from .base import NoteCommand


class ListCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='*', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        notes = self.filter_notes(options['filters']).all()

        if not notes:
            self.error_no_match()

        output = self.format(notes)
        self.cmd.stdout.write(output)

    def format(self, notes):
        headers = ['ID', 'Age', 'Project', 'Documents', 'Og', 'Rk', 'Text']
        lines = [headers]
        for note in notes:
            id = note.id
            age = note.age()  # self.note_age(note)
            proj = note.project
            project = proj.full_name() if proj else '-'
            docs = ",".join(d.name for d in note.documents.all()) or '-'
            rank = note.rank
            text = re.sub(r'\n+', '  ', note.text)
            original = '✓' if note.original else '✗'
            #original = colored('✓', 'green') if note.original else colored('✗', 'red')
            #created = note.created
            lines.append([id, age, project, docs, original, rank, text])

        table = TableBlock(lines, headers=['bold', 'underline'],
                           color_line='grey', max_line=1)

        return table.format()
