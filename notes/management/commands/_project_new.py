import os
from django.core.management.base import BaseCommand, CommandParser, CommandError
from argparse import FileType
from notes.models import Project
from ._functions import parse_project_name, get_or_create_project, get_project, create_note
from ._project_cmd import ProjectCommand


class NewCommand(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the project (computer friendly)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')

    def execute(self, args, options):
        names = options['name'].split('.')
        desc = options['description']

        proj, created, parent_id = None, None, None
        for name in names:
            proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
            parent_id = proj.id

        if not created:
            self.notify_already_exists(options['name'])

        if desc:
            proj.description = desc
            proj.save()

        self.notify_created(proj)
