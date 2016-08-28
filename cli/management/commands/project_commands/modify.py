from projects.models import Project
from projects.helpers import get_project, get_or_create_project
from .base import ProjectCommand


class ModifyCommand(ProjectCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the project')

    def execute(self, args, options):
        name_or_id = options['name_or_id']

        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        old_name, merged, desc_mod = None, False, False
        new_name = options['new_name']

        if new_name and new_name != proj.full_name():
            self.check_project_name_is_valid(new_name)
            old_name = proj.full_name()

            dest = get_project(new_name)
            if dest:
                # @fixme create #prompt_merge_projects
                create = input('The project `%s` already exists. Merge projects ? (no) ' % new_name)
                if create.lower() in ['', 'n', 'no']:
                    exit(1)
                else:
                    merged = True
                    # @fixme create #merge_projects
                    for note in proj.notes.all():
                        note.project = dest
                        note.save()

                    proj.delete()
                    proj = dest
            else:
                # @fixme create #create_project_recursively
                *parents, base_name = new_name.split('/')
                parent_name = "/".join(parents)

                if parent_name:
                    parent, _ = get_or_create_project(parent_name)
                else:
                    parent = None

                proj.name = base_name
                proj.parent = parent

        desc = options['description']
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
