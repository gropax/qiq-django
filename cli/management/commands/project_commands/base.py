import sys
import re
from qiq.common import SUCCESS, NOT_FOUND, EXISTS, INVALID
from projects.models import Project
from projects.helpers import parse_project_name, get_project, project_name_is_valid
from cli.management.commands._subcommand import Subcommand


class ProjectCommand(Subcommand):

    def success_project_created(self, project):
        self.success('Created project `%s`' % project.full_name())
        sys.exit(SUCCESS)

    def error_project_not_found(self, name):
        self.error("Project `%s` doesn't exist" % name)
        sys.exit(NOT_FOUND)

    def error_project_already_exists(self, name):
        self.error("Project `%s` already exists" % name)
        sys.exit(EXISTS)

    def error_invalid_project_name(self, name, interactive=False):
        self.error("Invalid project name: %s" % name)
        if not interactive:
            sys.exit(INVALID)

    def error_invalid_project_name_or_id(self, name_or_id):
        self.error("Invalid project name or id: %s" % name_or_id)
        sys.exit(INVALID)


    def check_project_name_is_valid(self, name):
        if not project_name_is_valid(name):
            self.error_invalid_project_name(name)


    def find_project_by_name_or_id_or_error(self, name_or_id):
        name_or_id = str(name_or_id)
        if re.match(r'^[0-9]+$', name_or_id):
            q = {'id': int(name_or_id)}
        elif project_name_is_valid(str(name_or_id)):
            q = {'name': name_or_id}
        else:
            self.error_invalid_project_name_or_id(name_or_id)

        try:
            return Project.objects.get(**q)
        except:
            self.error_project_not_found(name_or_id)
