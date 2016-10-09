from django.core.exceptions import ObjectDoesNotExist
from core.cli.command import Command, command
from projects.cli.utils import Utils
from projects.cli.commands.project import ProjectCommand
from projects.models import Project
from projects.cli import utils2 as prj


@command('modify', ProjectCommand)
class ModifyCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the project')

    def action(self, args):
        name_or_id = args.name_or_id

        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        old_name, merged, desc_mod = None, False, False
        new_name = args.new_name

        if new_name and new_name != proj.full_name():
            self.check_project_name_is_valid(new_name)
            old_name = proj.full_name()

            try:
                dest = prj.get_by_fullname(new_name)
                msg = 'The project `%s` already exists. Merge projects ?' % new_name
                if self.ask(msg, 'no'):
                    merged = True
                    proj = prj.merge(proj, dest)
                else:
                    exit(1)

            except ObjectDoesNotExist:
                prj.rename(proj, new_name)

        desc = args.description
        if desc and desc != proj.description:
            desc_mod = True
            proj.description = desc

        if old_name or desc_mod:
            proj.save()
            self.success_project_modified(proj, old_name, merged, desc_mod)
        else:
            self.warning_nothing_to_do()

    def success_project_modified(self, proj, old_name, merged, desc_mod):
        if old_name:
            if merged:
                action = "merged with"
            else:
                action = "renamed to"
            s = "Project `%s` %s `%s`" % (old_name, action, proj.full_name())
            if desc_mod:
                s += " and modified"
        else:
            s = "Project `%s` modified" % proj.full_name()

        self.success(s)
