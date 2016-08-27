import sys
import re
from notes.models import Note
from qiq.common import SUCCESS, INVALID, EXISTS, NOT_FOUND
import projects.management.commands._subcommand as sub


class Subcommand(sub.Subcommand):

    ############################
    ## Terminal output methods #
    ############################

    def error_note_not_found(self, note_id):
        self.error("Note %s doesn't exist" % note_id)
        sys.exit(NOT_FOUND)


    ###############################
    # Find models or return error #
    ###############################

    def find_note_by_id_or_error(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.error_note_not_found(note_id)
