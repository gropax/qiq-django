from core.cli.command import Command, command
from core.cli.commands.qiq import QiqCommand
from core.cli.utils import Utils
from core.cli.management import ManagementTasks
from termblocks import TextBlock, TableBlock, MarginBlock, VerticalLayout
from core.cli.format import format_table, list_table, format_cell, headers_data, format_completion


@command('manage', QiqCommand)
class ManageCommand(Command, Utils):
    help = 'Help improve database quality'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--perform', metavar='TASK',
                            help='execute management tasks')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--by-model', action='store_true')
        group.add_argument('--by-task', action='store_false')

    def action(self, args):
        self.tasks = ManagementTasks()
        self.task_types = self.tasks.types()

        if args.perform:
            names = args.perform.split(".")
            tasks = self.tasks.get(names)

            if isinstance(tasks, list):
                iterator = tasks.__iter__()
            else:
                if args.by_task:
                    iterator = tasks.by_task()
                else:
                    iterator = tasks.by_model()

            for task in iterator:
                task.perform()
        else:
            self.stdout.write(self.format_tasks(self.task_types))

    def check_management_task_exists(self, name):
        names = set(name for name, *_ in self.task_types)
        if not name in names:
            self.not_found("Task does not exist `%s`" % name)

    def format_tasks(self, tasks):
        headers = ['Name', 'Nb', 'Comp', 'Description']
        data = []
        for name, task_type, nb, comp in tasks:
            data.append([
                name,
                nb,
                format_completion(comp),
                task_type.description,
            ])

        rows = [headers_data(headers)]
        for values in data:
            cells = [format_cell(v) for v in values]
            options = {}
            rows.append({'cells': cells, 'options': options})

        return format_table(rows).format()
