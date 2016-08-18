from django.core.management.base import BaseCommand, CommandParser, CommandError
from datetime import datetime
from notes.models import Project
from ._functions import parse_project_name, get_project


class Subcommand(object):
    def __init__(self, cmd):
        self.cmd = cmd
