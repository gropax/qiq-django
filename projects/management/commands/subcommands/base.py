from django.core.management.base import BaseCommand, CommandParser, CommandError
from datetime import datetime
from projects.models import Project
from notes.management.commands._functions import parse_project_name, get_project


class ProjectCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd

    def notify_created(self, project):
        s = 'Created project `%s`' % project.full_name()
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def notify_not_found(self, name):
        s = "Project `%s` doesn't exist" % name
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        exit(1)

    def notify_already_exists(self, name):
        s = "Project `%s` already exists" % name
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        exit(1)

    def notify_no_match(self):
        s = "No matches."
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        exit(1)
