import re
from notes.models import Project


def parse_project_name(name):
    return name.lower().split('/')

def get_or_create_project(name, desc=''):
    proj, created, parent_id = None, None, None

    for name in parse_project_name(name):
        proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
        parent_id = proj.id

    if created:
        proj.description = desc
        proj.save()

    return proj, created

def get_all_projects():
    return Project.objects.all()

def get_project(name):
    """Return `Project` object corresponding to the given name, or `None` if
    it doesn't exist"""
    proj, parent_id = None, None

    for name in parse_project_name(name):
        try:
            proj = Project.objects.get(user_id=1, parent_id=parent_id, name=name)
        except:
            return None

        parent_id = proj.id

    return proj

# Project's name begin with a letter, may contain numbers and slashs, cannot end
# with a slash. All letters are lower case.
PROJNAME_re = re.compile(r'^[a-z][_a-z0-9]*(?:\/[a-z][_a-z0-9]*)*$')

def project_name_is_valid(name):
    return PROJNAME_re.match(name)
