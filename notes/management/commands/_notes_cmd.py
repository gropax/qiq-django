from django.core.management.base import BaseCommand, CommandParser, CommandError
import re
from notes.models import Note, Project
from ._functions import parse_project_name, filter_query, get_project


VTAGS = ['ORIGINAL']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:([a-z]+(?:\.[a-z]+)*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')


class NoteCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def notify_creation(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def notify_not_found(self, id):
        s = "Note %s doesn't exist" % id
        self.cmd.stdout.write(self.cmd.style.ERROR(s))

    def notify_empty_set(self):
        s = "No matches."
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        exit(1)

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

    def filter_query(self, filters):
        ids, proj_name, vtags = set(), None, {}

        for f in filters:
            if IDS_re.match(f):
                ids.update(int(i) for i in f.split(','))
                continue

            m = PROJ_re.match(f)
            if m:
                proj_name = m.group(1)
                continue

            m = VTAG_re.match(f)
            if m:
                sign, vtag = m.group(1), m.group(2)
                if vtag in VTAGS:
                    vtags[vtag] = True if sign == '+' else False
                else:
                    self.cmd.stderr.write(self.cmd.style.ERROR("Unknown virtual tag `%s`" % vtag))
                    exit(1)

        q = {}
        if ids: q['id__in'] = list(ids)

        if proj_name:
            proj = get_project(proj_name)
            if proj:
                q['project'] = proj
            else:
                self.cmd.stderr.write(self.cmd.style.ERROR("Unknown project `%s`" % project.full_name()))
                exit(1)

        if 'ORIGINAL' in vtags:
            q['original'] = vtags['ORIGINAL']

        return q
