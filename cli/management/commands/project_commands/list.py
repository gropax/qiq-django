from termblocks import TableBlock
from projects.models import Project
from .base import ProjectCommand


class ListCommand(ProjectCommand):
    def add_arguments(self, parser):
        pass

    def execute(self, args, options):
        projs = Project.objects.filter(user_id=1).all()

        if not projs.all():
            self.error_no_match()

        sort = sorted(projs, key=lambda p: p.full_name())

        output = self.format(sort)
        self.cmd.stdout.write(output)

    def format(self, projs):
        headers = ['ID', 'Name', 'Notes', 'Description']
        table = self.list_table(headers, projs, self.list_row_data)
        return table.format()

    def list_row_data(self, proj):
        return [
            proj.id,
            self.format_project_name(proj),
            proj.notes.count(),
            proj.description, # or '*',
        ]

    #def format(self, projs):
        #headers = ['ID', 'Name', 'Notes', 'Description']
        #lines = [headers]
        #for proj in projs:
            #id = proj.id
            #name = proj.full_name()
            #notes = proj.notes.count()
            #desc = proj.description
            #lines.append([id, name, notes, desc])

        #table = TableBlock(lines, headers=['bold', 'underline'],
                           #color_line='grey', max_line=1)

        #return table.format()
