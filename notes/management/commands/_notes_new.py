import os
import tempfile
import subprocess
from django.core.management.base import BaseCommand, CommandParser, CommandError
from argparse import FileType
from ._functions import parse_project_name, get_or_create_project, get_project, create_note


class NewCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd

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

    def get_or_prompt_project(self, options):
        if options['no_project']:
            proj = None
        else:
            if options['project']:
                name = options['project']
            else:
                # @todo Add auto complete
                name = input('Project: ')
                if not name:
                    return None

            if options['create_project']:
                proj = get_or_create_project(name)
            else:
                proj = get_project(name)
                if not proj:
                    self.cmd.stdout.write("The project `%s` doesn't exist." % name)
                    create = input('Create it ? (yes) ')
                    if create.lower() in ['', 'y', 'ye', 'yes']:
                        proj = get_or_create_project(name)
                    else:
                        exit(1)
        return proj

    def execute(self, args, options):
        proj = self.get_or_prompt_project(options)

        if options['infile']:
            f = options['infile']
        else:
            _, f = tempfile.mkstemp()
            subprocess.call(['vim', f, '-u', 'NONE', '-c', 'startinsert'])

            # @fixme Use custom editor command
            #cmd = options['editor'].replace('%', f)
            #subprocess.call(cmd)

        with open(f, 'r') as file:
            text = file.read()

        if text:
            note = create_note(proj, text)
            self.notify_creation(note)
        else:
            exit(1)

    def notify_creation(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))
