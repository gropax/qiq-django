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
