from django.core.management.base import BaseCommand, CommandParser, CommandError
import re
from termcolor import colored
from notes.models import Project
from ._term_blocks import TableBlock
from ._project_cmd import ProjectCommand


class ListCommand(ProjectCommand):
    def add_arguments(self, parser):
        pass

    def execute(self, args, options):
        projs = Project.objects.filter(user_id=1).all()

        if not projs.all():
            self.notify_no_match()

        sort = sorted(projs, key=lambda p: p.full_name())

        output = self.format(sort)
        self.cmd.stdout.write(output)

    def format(self, projs):
        headers = ['ID', 'Name', 'Notes', 'Description']
        lines = [headers]
        for proj in projs:
            id = proj.id
            name = proj.full_name()
            notes = proj.notes.count()
            desc = proj.description
            lines.append([id, name, notes, desc])

        table = TableBlock(lines, headers=['bold', 'underline'],
                           color_line='grey', max_line=1)

        return table.format()
