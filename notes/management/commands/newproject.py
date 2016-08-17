from django.core.management.base import BaseCommand, CommandError
from notes.models import Project


class Command(BaseCommand):
    help = 'Create a new project'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str,
                            help='the name of the project (computer friendly)')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the project')

    def handle(self, *args, **options):
        names = options['name'].split('.')
        desc = options['description']

        proj, created, parent_id = None, None, None
        for name in names:
            proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
            parent_id = proj.id

        if not created:
            self.stdout.write(self.style.ERROR('Project "%s" already exists' % proj))
            exit(1)

        if desc:
            proj.description = desc
            proj.save()
            self.stdout.write(self.style.SUCCESS('Created project %s' % proj))
