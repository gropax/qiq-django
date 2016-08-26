import os
from django.core.management.base import BaseCommand, CommandParser, CommandError
from argparse import FileType
from projects.helpers import parse_project_name, get_or_create_project, get_project
from notes.helpers import create_note
from .base import NoteCommand


class NewCommand(NoteCommand):
    def add_arguments(self, parser):
        input_grp = parser.add_mutually_exclusive_group()
        #input_grp.add_argument('-e', '--editor', type=str,
                                #default='vim % -u NONE -c startinsert',
                                #help='the command used to open the editor')
        input_grp.add_argument('-f', '--infile', type=FileType('r'),
                                help='the file containing the text of the note')

        proj_grp = parser.add_mutually_exclusive_group()
        proj_grp.add_argument('-p', '--project', type=str,
                                help='the project in which to store the note')
        proj_grp.add_argument('-P', '--no-project', action='store_true', default=False,
                                help='do not store the note in any project')
        parser.add_argument('-c', '--create-project', action='store_true', default=False,
                                help='create the project if it doesn\'t exist')

    def execute(self, args, options):
        proj = self.get_or_prompt_project(options)

        if options['infile']:
            f = options['infile']
        else:
            f = self.edit_note_in_editor(options)

        with open(f, 'r') as file:
            text = file.read()

        if text:
            note = create_note(proj, text)
            self.notify_creation(note)
        else:
            exit(1)
