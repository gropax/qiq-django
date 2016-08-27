import sys
import re


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

    def warning_nothing_to_do(self):
        self.warning("Nothing to do")
        sys.exit(0)
