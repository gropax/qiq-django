from core.cli.command import Command, command
from projects.cli.commands.project import ProjectCommand
from projects.cli.utils import Utils


@command('delete', ProjectCommand)
class DeleteCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the project')

    def action(self, args):
        name_or_id = args.name_or_id
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        proj.delete()
        self.success_project_deleted(proj)
