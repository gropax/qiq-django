import sys
import re
from notes.models import Document, Note


# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

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
        sys.exit(1)

    def error_note_not_found(self, note_id):
        self.error("Note %s doesn't exist" % note_id)
        sys.exit(1)

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")
        sys.exit(0)


    ###############################
    # Find models or return error #
    ###############################

    def find_note_by_id_or_error(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.error_note_not_found(note_id)
            sys.exit(1)
