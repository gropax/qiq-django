import sys
import re
from projects.models import Project
from projects.helpers import parse_project_name, get_project
from projects.management.commands._subcommand import Subcommand


# Project's name begin with a letter, may contain numbers and slashs, cannot end
# with a slash. All letters are lower case.
PROJNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\/[a-z][a-z0-9]*)*$')

class ProjectCommand(Subcommand):

    def success_project_created(self, project):
        self.success('Created project `%s`' % project.full_name())
        exit(0)

    def error_project_not_found(self, name):
        self.error("Project `%s` doesn't exist" % name)
        exit(1)

    def error_project_already_exists(self, name):
        self.error("Project `%s` already exists" % name)
        exit(1)

    def error_invalid_project_name(self, name):
        self.error("Invalid project name: %s" % name)
        sys.exit(30)


    def check_project_name_is_valid(self, name):
        if not PROJNAME_re.match(name):
            self.error_invalid_project_name(name)
