from django.core.management.base import BaseCommand, CommandError
from notes.models import Note


class Command(BaseCommand):
    help = 'List all notes'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        notes = Note.objects.filter(user_id=1)
        for note in list(notes):
            l = len(note.text)
            preview = ("%i\t%i\t%i" % (note.id, note.rank, note.original)) + '\t' + note.text[:50].replace('\n', ' '*4) + ('...' if l > 50 else '')
            self.stdout.write(preview)
