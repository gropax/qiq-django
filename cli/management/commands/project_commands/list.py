from termblocks import TableBlock
from projects.models import Project
from .base import ProjectCommand
from cli.format import list_table, format_project_name, format_project_note_no


class ListCommand(ProjectCommand):
    def add_arguments(self, parser):
        pass

    def execute(self, args, options):
        projs = Project.objects.filter(user_id=1).all()

        if not projs.all():
            self.error_no_match()

        sort = sorted(projs, key=lambda p: p.full_name())

        output = self.format(sort)
        self.cmd.stdout.write(output)

    def format(self, projs):
        headers = ['ID', 'Name', 'Notes', 'Description']
        table = list_table(headers, projs, self.list_row_data)
        return table.format()

    def list_row_data(self, proj):
        return [
            proj.id,
            format_project_name(proj),
            format_project_note_no(proj.notes.count()),
            proj.description, # or '*',
        ]
