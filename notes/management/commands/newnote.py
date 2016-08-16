import os
import sys
import tempfile
import subprocess
from django.core.management.base import BaseCommand, CommandError
from notes.models import Note


class Command(BaseCommand):
    help = 'Create a new note'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--interactive', action='store_true',
                            help='edit the note in a text editor')

    def handle(self, *args, **options):
        text = None

        if options['interactive']:
            _, tmp = tempfile.mkstemp()
            subprocess.call(['vim', tmp, '-u', 'NONE', '-c', 'startinsert'])

            with open(tmp, 'r') as tmpf:
                text = tmpf.read()
        else:
            pass

        if text:
            note = Note(user_id=1, text=text)  # @fixme user_id
            note.save()
            self.stdout.write(self.style.SUCCESS('Created note %s' % note.id))
        else:
            exit(1)
