import os
from django.core.management.base import BaseCommand, CommandParser, CommandError
from projects.models import Project
from projects.helpers import get_project, get_or_create_project
from .base import ProjectCommand


class ModifyCommand(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the project (fully qualified)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the project')

    def notify_merged(self, proj, dest):
        s = "Merged projects `%s` and `%s`" % (proj.full_name(), dest.full_name())
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def notify_renamed(self, name, new_name):
        s = "Renamed project `%s` to `%s`" % (name, new_name)
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def notify_modified(self, proj):
        s = "Modified project `%s`" % (proj.full_name())
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def execute(self, args, options):
        name = options['name']

        proj = get_project(name)
        if not proj:
            self.notify_not_found(name)

        new_name = options['new_name']
        if new_name:
            dest = get_project(new_name)
            if dest:
                create = input('The project `%s` already exists. Merge projects ? (no) ' % new_name)
                if create.lower() in ['', 'n', 'no']:
                    exit(1)
                else:
                    for note in proj.notes.all():
                        note.project = dest
                        note.save()

                    proj.delete()
                    self.notify_merged(proj, dest)
                    proj = dest
            else:
                *parents, base_name = new_name.split('.')
                parent_name = ".".join(parents)

                if parent_name:
                    parent, _ = get_or_create_project(parent_name)
                else:
                    parent = None

                proj.name = base_name
                proj.parent = parent
                self.notify_renamed(name, new_name)

        desc = options.get('description', None)
        if desc:
            proj.description = desc
            self.notify_modified(proj)

        proj.save()
