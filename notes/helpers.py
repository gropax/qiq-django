from notes.models import Note
import re


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
