import re
from django.core.exceptions import ObjectDoesNotExist
from projects.models import Project


def get_all_projects():
    return Project.objects.all()

def get_by_name_recursively(names):
    proj, parent_id = None, None

    for name in names:
        try:
            proj = Project.objects.get(user_id=1, parent_id=parent_id, name=name)
        except:
            raise ObjectDoesNotExist("name `%s`" % name)
        parent_id = proj.id

    return proj

def get_or_create_recursively(names, desc=''):
    proj, created, parent_id = None, None, None

    for name in names:
        proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
        parent_id = proj.id

    if created:
        proj.description = desc
        proj.save()

    return proj, created
