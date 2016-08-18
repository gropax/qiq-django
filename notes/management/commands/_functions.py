from notes.models import Note, Project
import re


def parse_project_name(name):
    return name.lower().split('.')

def get_or_create_project(name, desc=''):
    proj, created, parent_id = None, None, None

    for name in parse_project_name(name):
        proj, created = Project.objects.get_or_create(user_id=1, parent_id=parent_id, name=name)
        parent_id = proj.id

    proj.description = desc
    proj.save()

    return proj

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

# @fixme user_id
#
def create_note(proj, text):
    note = Note(user_id=1, project=proj, text=text)
    note.save()
    return note

def merge_notes(proj, text, notes):
    rank = 0
    for n in notes:
        rank += n.rank
        n.original = False
        n.save()

    note = Note(user_id=1, project=proj, text=text, rank=rank)
    note.save()
    note.references.add(*notes)
    return note

def virtual_tags(note):
    tags = []
    if note.original: tags.append('ORIGINAL')
    return tags

VTAGS = ['ORIGINAL']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:([a-z]+(?:\.[a-z]+)*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')

def filter_query(filters):
    ids, proj, vtags = set(), None, {}

    for f in filters:
        if IDS_re.match(f):
            ids.update(int(i) for i in f.split(','))
            continue

        m = PROJ_re.match(f)
        if m:
            proj = m.group(1)
            continue

        m = VTAG_re.match(f)
        if m:
            sign, vtag = m.group(1), m.group(2)
            vtags[vtag]
            continue

    print(ids)

