from projects.models import Project
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from .base import ProjectCommand


class InfoCommand(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        output = self.format(proj)
        self.cmd.stdout.write(output)

    def format_info(self, proj):
        table = TableBlock([
            ['Name',       'Value'],
            ['ID',          proj.id],
            ['Name',        proj.full_name()],
            ['Description', proj.description],
            ['Notes',       proj.notes.count()],
        ], headers=['bold', 'underline'], color_line='grey')

        return table.format()

    def format(self, proj):
        table = self.model_table([
            ['ID', proj.id],
            ['Name', self.format_project_name(proj)],
            ['Description', self.format_project_description(proj)],
            ['Notes', proj.notes.count()],
        ])
        return table.format()
