from projects.models import Project
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from .base import ProjectCommand
from cli.format import model_table, format_project_name, format_project_description, format_project_note_no


class InfoCommand(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        output = self.format(proj)
        self.cmd.stdout.write(output)

    def format(self, proj):
        table = model_table([
            ['ID', proj.id],
            ['Name', format_project_name(proj)],
            ['Description', format_project_description(proj)],
            ['Original notes', format_project_note_no(proj.notes.filter(original=True).count())],
            ['Old notes', proj.notes.filter(original=False).count()],
        ])
        return table.format()
