import readline
import re
from django.core.exceptions import ObjectDoesNotExist
from core.cli.utils import Utils as Base
from projects.cli import utils2 as prj
from projects.models import Project

PROJECT_FULLNAME_re = re.compile(r'^[a-z][_a-z0-9]*(?:\/[a-z][_a-z0-9]*)*$')


class Utils(Base):
    def success_project_created(self, project):
        self.success('Created project `%s`' % project.full_name())

    def success_project_deleted(self, proj):
        self.success("Project `%s` deleted" % proj.name)

    def error_project_already_exists(self, name):
        self.already_exists("Project `%s` already exists" % name)

    def error_invalid_project_name(self, name, interactive=False):
        self.invalid("Invalid project name: %s" % name, interactive=False)

    def error_invalid_project_name_or_id(self, name_or_id):
        self.invalid("Invalid project name or id: %s" % name_or_id)

    def error_project_not_found(self, name):
        self.not_found("Project `%s` doesn't exist" % name)


    # @fixme
    def find_project_by_id(self, proj_id):
        proj_id = int(proj_id)
        return self.find_project_by_name_or_id(proj_id)

    def find_project_by_id_or_error(self, proj_id):
        try:
            return self.find_project_by_id(proj_id)
        except ObjectDoesNotExist as e:
            self.error_project_not_found(proj_id)

    def find_project_by_name_or_id(self, name_or_id):
        return prj.get_by_fullname_or_id(name_or_id)

    def find_project_by_name_or_id_or_error(self, name_or_id):
        try:
            return prj.get_by_fullname_or_id(name_or_id)
        except ValueError as e:
            self.error_invalid_project_name_or_id(name_or_id)
        except ObjectDoesNotExist as e:
            self.error_project_not_found(name_or_id)


    # Projects
    #
    #def get_or_prompt_project(self, project=None, no_project=False, default=None, create_project=False):
        #if no_project:
            #proj = None
        #else:
            #if project:
                #name = project
                #self.check_project_name_is_valid(name)
            #else:
                #if default and self.ask('Use project `%s` ?' % default.full_name(), default='yes'):
                    #return default
                #name = self.prompt_project()

            #if not name:
                #return None

            #if project and create_project:
                #proj, _ = prj.get_or_create_recursively(name)
            #else:
                #try:
                    #proj = prj.get_by_fullname(name)
                #except ObjectDoesNotExist:
                    #if self.ask('Project `%s` does not exist. Create it ?' % name, default='yes'):
                        #proj, _ = prj.get_or_create_recursively(name)
                    #else:
                        #self.warning_operation_aborted()
        #return proj

    def create_project(self, fullname):
        proj, _ = prj.get_or_create_recursively(fullname)
        return proj

    def get_or_prompt_project(self, project=None, default=None, create_project=False):
        name = None

        if project:
            project = str(project)
            if re.match('^[0-9]$', project):
                return self.find_project_by_id_or_error(project)
            elif PROJECT_FULLNAME_re.match(project):
                try:
                    return self.find_project_by_name_or_id(project)
                except ObjectDoesNotExist:
                    if create_project or self.ask('Project `%s` does not exist. Create it ?' % name, default='yes'):
                        name = project
                    else:
                        self.warning_operation_aborted()
            else:
                self.error_invalid_project_name(project)
        else:
            if default and self.ask('Use project `%s` ?' % default.full_name(), default='yes'):
                return default

            name = self.prompt_project()

        if name:
            return self.create_project(name)
        else:
            return None

    def set_project_autocomplete(self):
        completer = self.project_completer()

        # Remove / from delimiter to complete project full_name
        delims = readline.get_completer_delims()
        readline.set_completer_delims(delims.replace('/', ''))

        readline.set_completer(completer.complete)
        readline.parse_and_bind('tab: complete')

    def project_completer(self):
        projs = Project.objects.filter(user_id=1)
        names = [proj.full_name() for proj in projs.all()]
        return AutoCompleter(names)

    def prompt_project(self):
        self.set_project_autocomplete()

        while True:
            name = input('Project: ')
            if not name:
                return None
            elif prj.name_is_valid(name):
                return name
            else:
                self.error_invalid_project_name(name, interactive=True)


    def check_project_name_is_valid(self, name):
        if not prj.name_is_valid(name):
            self.error_invalid_project_name(name)



class AutoCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options
                                  if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


