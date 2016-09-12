from django.core.management.base import BaseCommand
from django.db.models import Count
from projects.models import Project
from collections import defaultdict
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from cli.format import headers_data, format_table, model_row_data


class Command(BaseCommand):
    help = 'Help improve database quality'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--list', action='store_true', default=False,
                            help='list the pending management tasks')

    def handle(self, *args, **options):
        tasks = self.compute_management_tasks()

        if options['list']:
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
        return tasks

    def format_tasks(self, tasks):
        headers = ['Task', 'Nb']
        data = [
            ['Add project description',  len(tasks['descriptions'])],
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

    #def manage_project_descriptions(self):
        #projs = Project.objects.filter(user_id=1, description='').all()
        #sort = sorted(projs, key=lambda p: p.full_name())

        #self.stdout.write("Managing Projects\n=================\n")

        #for p in sort:
            #desc = input("Enter a description for `%s`  (pass) " % p.full_name())
            #if desc:
                #p.description = desc
                #p.save()


class ProjectAddDescription(object):
    def __init__(self, proj):
        self.project = proj

    def perform(self):
        desc = input("Enter a description for `%s`  (pass) " % self.project.full_name())
        if desc:
            self.project.description = desc
            self.project.save()
