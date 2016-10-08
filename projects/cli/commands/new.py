from core.cli.command import Command, command
from projects.cli.utils import Utils
from projects.cli.commands.project import ProjectCommand
from projects.models import Project


@command('new', ProjectCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the project (computer friendly)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')

    def action(self, args):
        name = args.name
        self.check_project_name_is_valid(name)

        # @fixme create #create_project_recursively_or_error
        #---
        names = args.name.split('/')
        proj, created, parent_id = None, None, None
        for name in names:
            proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
            parent_id = proj.id

        if not created:
            self.error_project_already_exists(args.name)
        #---

        desc = args.description
        if desc:
            proj.description = desc
            proj.save()

        self.success_project_created(proj)
