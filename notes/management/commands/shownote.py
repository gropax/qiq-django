from django.core.management.base import BaseCommand, CommandError
from notes.models import Note


class Command(BaseCommand):
    help = 'Show the details of a note'

    def add_arguments(self, parser):
        parser.add_argument('note_id', type=int,
                            help='the id of the note')

    def handle(self, *args, **options):
        note_id = options['note_id']
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            raise CommandError('Note "%s" does not exist' % note_id)

        s = "id:  %i\ncreated at:  %s\ncontent:\n%s\n" % (note.id, note.created, note.text)

        self.stdout.write(s)
