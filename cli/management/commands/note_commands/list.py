from django.core.management.base import BaseCommand, CommandParser, CommandError
import re
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
        table = self.list_table(headers, notes, self.list_row_data)
        return table.format()

    def list_row_data(self, note):
        return [
            note.id,
            note.age(),
            self.format_project_name(note.project),
            self.format_document_list(note),
            self.format_original(note),
            note.rank,
            self.format_text(note),
        ]
