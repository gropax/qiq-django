from cli.management.commands._subcommand import Subcommand
from projects.models import Project
import cli.format as f


class ListCommand(Subcommand):
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
