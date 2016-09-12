import sys
import re
from notes.models import Note
from projects.helpers import project_name_is_valid
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
from termblocks import TableBlock


class Subcommand(object):
    def __init__(self, cmd):
        self.cmd = cmd


    ###########################
    # Terminal output methods #
    ###########################

    def success(self, string):
        self.cmd.stdout.write(self.cmd.style.SUCCESS(string))

    def error(self, string):
        self.cmd.stdout.write(self.cmd.style.ERROR(string))

    def warning(self, string):
        self.cmd.stdout.write(self.cmd.style.WARNING(string))


    def error_no_match(self):
        self.error("No match")
        sys.exit(NOT_FOUND)

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")
        sys.exit(SUCCESS)

    def error_note_not_found(self, note_id):
        self.error("Note %s doesn't exist" % note_id)
        sys.exit(NOT_FOUND)

    def error_invalid_project_name(self, name, interactive=False):
        self.error("Invalid project name: %s" % name)
        if not interactive:
            sys.exit(INVALID)


    def check_project_name_is_valid(self, name):
        if not project_name_is_valid(name):
            self.error_invalid_project_name(name)


    ###############################
    # Find models or return error #
    ###############################

    def find_note_by_id_or_error(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.error_note_not_found(note_id)
