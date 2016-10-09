from core.cli.command import Command, command
from core.cli.commands.qiq import QiqCommand
from django.db.models import Count
from projects.models import Project
from collections import defaultdict
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from core.cli.format import headers_data, format_table, model_row_data


@command('manage', QiqCommand)
class ManageCommand(Command):
    help = 'Help improve database quality'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--list', action='store_true', default=False,
                            help='list the pending management tasks')

    def action(self, args):
        tasks = self.compute_management_tasks()

        if args.list:
            self.stdout.write(self.format_tasks(tasks))
        else:
            self.perform_tasks(tasks)

    def compute_management_tasks(self):
        tasks = defaultdict(list)

        projs = Project.objects.filter(user_id=1).all()
        sort = sorted(projs, key=lambda p: p.full_name())

        for proj in sort:
            if not proj.description:
                tasks['descriptions'].append(ProjectAddDescription(proj))
            if proj.notes.count() > 5:
                tasks['merge_notes'].append(ProjectMergeNotes(proj))
        return tasks

    def format_tasks(self, tasks):
        headers = ['Task', 'Nb']
        data = [
            ['Add project description',  len(tasks['descriptions'])],
            ['Merge notes in project',  len(tasks['merge_notes'])],
        ]
        rows = [headers_data(headers)]
        for label, value in data:
            rows.append(model_row_data(label, value))

        return format_table(rows).format()

    def perform_tasks(self, tasks):
        if tasks['descriptions']:
            self.print_task_title("Adding project descriptions")
            for task in tasks['descriptions']:
                task.perform()

    def print_task_title(self, title):
        s = "\n" + title + "\n" + "="*len(title) + "\n"
        self.stdout.write(s)


class ProjectAddDescription(object):
    def __init__(self, proj):
        self.project = proj

    def perform(self):
        # @fixme interactions
        desc = input("Enter a description for `%s`  (pass) " % self.project.full_name())
        if desc:
            self.project.description = desc
            self.project.save()


class ProjectMergeNotes(object):
    def __init__(self, proj):
        self.project = proj

    def perform(self):
        pass
        # @fixme interactions
        #yes = input("Do you want to merge notes in `%s` (no) " % self.project.full_name())
        #if yes:
            #self.project.description = desc
            #self.project.save()
