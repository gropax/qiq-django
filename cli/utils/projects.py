import re
import projects.utils as prj
from projects.models import Project  # @fixme Should it call Project directly ?


PROJECT_SEPARATOR = '/'

# Project's name begin with a letter, may contain numbers and slashs, cannot end
# with a slash. All letters are lower case.
PROJECT_FULLNAME_re = re.compile(r'^[a-z][_a-z0-9]*(?:\/[a-z][_a-z0-9]*)*$')

def name_is_valid(name):
    return PROJECT_FULLNAME_re.match(name)

def parse_name(name, sep=PROJECT_SEPARATOR):
    return name.lower().split(sep)

def rename(proj, new_name):
    *parents, base_name = new_name.split(PROJECT_SEPARATOR)
    parent_name = PROJECT_SEPARATOR.join(parents)

    if parent_name:
        parent, _ = get_or_create_project(parent_name)
    else:
        parent = None

    proj.name = base_name
    proj.parent = parent

def get_or_create_recursively(name, desc=''):
    names = parse_name(name)
    return prj.get_or_create_recursively(names, desc)

def get_by_fullname(name):
    if not name_is_valid(name):
        raise ValueError("Invalid project name `%s`" % name)
    names = parse_name(name)
    return prj.get_by_name_recursively(names)

def get_by_fullname_or_id(name_or_id):
    name_or_id = str(name_or_id)
    if re.match(r'^[0-9]+$', name_or_id):
        proj_id = int(name_or_id)
        return Project.objects.get(id=proj_id)
    else:
        return get_by_fullname(name_or_id)

def merge(p1, p2):
    for note in p1.notes.all():
        note.project = p2
        note.save()
    p1.delete()
    return p2
