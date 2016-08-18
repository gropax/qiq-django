from django.core.management.base import BaseCommand, CommandParser, CommandError
from notes.models import Note
from ._notes_cmd import NoteCommand


class DeleteCommand(NoteCommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        q = self.filter_query(options['filters'])
        no, _ = Note.objects.filter(**q).delete()
        if no:
            self.notify_deleted(no)
        else:
            self.notify_empty_set()

    def notify_deleted(self, n):
        notes = 'note' if n == 1 else 'notes'
        self.cmd.stdout.write(self.cmd.style.SUCCESS("%i %s deleted" % (n, notes)))
