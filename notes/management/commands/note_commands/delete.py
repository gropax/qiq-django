from django.core.management.base import BaseCommand, CommandParser, CommandError
from notes.models import Note
from .base import NoteCommand


class DeleteCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        notes = self.filter_notes(options['filters'])

        no, _ = notes.delete()
        if no:
            self.success_notes_deleted(no)
        else:
            self.error_no_match()
