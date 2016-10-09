from core.cli.command import Command, command
from projects.cli.utils import Utils
from projects.cli.commands.project import ProjectCommand
from projects.models import Project
import core.cli.format as f


@command('info', ProjectCommand)
class InfoCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')

    def action(self, args):
        name_or_id = args.name_or_id
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        output = self.format(proj)
        self.stdout.write(output)

    def format(self, proj):
        table = f.model_table([
            ['ID', proj.id],
            ['Name', f.format_project_name(proj)],
            ['Description', f.format_project_description(proj)],
            ['Original notes', f.format_project_note_no(proj.notes.filter(original=True).count())],
            ['Old notes', proj.notes.filter(original=False).count()],
        ])
        return table.format()
