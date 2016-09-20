from cli.management.commands._subcommand import Subcommand


class DeleteCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the project')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        proj.delete()
        self.success_project_deleted(proj)
