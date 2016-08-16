import os
import tempfile
import subprocess
from django.core.management.base import BaseCommand, CommandError
from notes.models import Note


class Command(BaseCommand):
    help = 'Create a new note by aggregating existing notes'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--filters', nargs='+',
                            help='select the notes to merge together')

    def handle(self, *args, **options):
        # Fetch notes. For now, filters is only a list of ids separated by a
        # comma, ex: 1,43,27
        idstr = options['filters'][0]
        ids = [int(id) for id in idstr.split(',')]
        notes = Note.objects.filter(pk__in=ids)

        # Make tmp
        _, tmp = tempfile.mkstemp()

        # Write notes in tmp
        text = "\n\n".join(note.text for note in notes)
        with open(tmp, 'w') as tmpf:
            tmpf.write(text)

        # Edit tmp
        subprocess.call(['vim', tmp, '-u', 'NONE', '-c', 'startinsert'])

        # Read tmp
        with open(tmp, 'r') as tmpf:
            text = tmpf.read()

        # Created new note
        if text:
            note = Note(user_id=1, text=text)  # @fixme user_id
            note.save()
            note.references.add(*notes)
            self.stdout.write(self.style.SUCCESS('Created note %s' % note.id))
        else:
            exit(1)
