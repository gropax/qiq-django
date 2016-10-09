from core.cli.command import Command, command
from projects.cli.utils import Utils
from projects.cli.commands.project import ProjectCommand
from projects.models import Project
import core.cli.format as f


@command('list', ProjectCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        pass

    def action(self, args):
        projs = Project.objects.filter(user_id=1).all()

        if not projs.all():
            self.error_no_match()

        sort = sorted(projs, key=lambda p: p.full_name())

        output = self.format(sort)
        self.stdout.write(output)

    def format(self, projs):
        headers = ['ID', 'Name', 'Original', 'Description']
        table = f.list_table(headers, projs, self.list_row_data)
        return table.format()

    def list_row_data(self, proj):
        return [
            proj.id,
            f.format_project_name(proj),
            f.format_project_note_no(proj.notes.filter(original=True).count()),
            proj.description, # or '*',
        ]
