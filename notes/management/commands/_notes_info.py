from textwrap import TextWrapper
from django.core.management.base import BaseCommand, CommandParser, CommandError
from notes.models import Note
#from argparse import FileType
from termcolor import colored


INDENT = ' ' * 4

HEADERS = colored("Name            Value".ljust(60), None, attrs=['bold', 'underline'])
TEMPLATE = """ID              %i
User            %s
Project         %s
Created         %s
Original        %s
Previous notes  %s
Next notes      %s
Rank            %i"""

class InfoCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        try:
            note = Note.objects.get(id=options['id'])
        except:
            self.notify_not_found(id)
            exit(1)

        output = self.format_info(note)
        self.cmd.stdout.write(output)

    def notify_not_found(self, id):
        s = "Note %s doesn't exist" % id
        self.cmd.stdout.write(self.cmd.style.ERROR(s))

    def format_info(self, note):
        id = note.id
        username = note.user.username
        proj = note.project
        project = proj.full_name() if proj else '-'
        created = note.created
        fresh = True if note.original else False
        prev = ",".join(str(n.id) for n in note.references.all()) or '-'
        next = ",".join(str(n.id) for n in note.referencers.all()) or '-'
        rank = note.rank

        metadata_lines = [HEADERS] + (TEMPLATE % (id, username, project, created, fresh, prev, next, rank)).split('\n')
        metadata = "\n".join(l.ljust(60) for l in metadata_lines)

        wrapper = TextWrapper(width=52)
        content_lines = ["Content",""] + [INDENT + line for line in wrapper.wrap(note.text)]
        content = "\n".join(l.ljust(60) for l in content_lines)

        lines = metadata.split('\n') + [content]
        color = []
        dark = not len(lines) % 2
        for line in lines:
            if dark:
                color.append(colored(line, None, 'on_grey'))
            else:
                color.append(line)
            dark = not dark

        return "\n".join(color) + "\n\n"
