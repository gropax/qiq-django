import readline
from django.core.exceptions import ObjectDoesNotExist
from core.cli.utils import Utils as Base
import cli.utils.projects as prj
from projects.models import Project


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



    def find_project_by_name_or_id_or_error(self, name_or_id):
        try:
            return prj.get_by_fullname_or_id(name_or_id)
        except ValueError as e:
            self.error_invalid_project_name_or_id(name_or_id)
        except ObjectDoesNotExist as e:
            self.error_project_not_found(name_or_id)


    # Projects
    #
    def get_or_prompt_project(self, args, default=None):
        if args.no_project:
            proj = None
        else:
            if args.project:
                name = args.project
                self.check_project_name_is_valid(name)
            else:
                if default and self.ask('Use project `%s` ?' % default.full_name(), default='yes'):
                    return default
                name = self.prompt_project()

            if not name:
                return None

            if args.project and args.create_project:
                proj, _ = prj.get_or_create_recursively(name)
            else:
                try:
                    proj = prj.get_by_fullname(name)
                except ObjectDoesNotExist:
                    if self.ask('Project `%s` does not exist. Create it ?' % name, default='yes'):
                        proj, _ = prj.get_or_create_recursively(name)
                    else:
                        self.warning_operation_aborted()
        return proj

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


