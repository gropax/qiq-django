import pytz
import sys
import os
import re
import tempfile
import subprocess
import shlex
import datetime
from projects.cli import utils2 as prj
from projects.cli.utils import Utils as Base
from notes.models import Note, Document
from notes.helpers import merge_notes
from django.core.exceptions import ObjectDoesNotExist

# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

VTAGS = ['ORIGINAL', 'DOCUMENT']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:((?:[0-9]+)|(?:[a-z][a-z0-9]+(?:\/[a-z][a-z0-9]+))*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')

NOTE_ATTRIBUTES = ['text']


class Utils(Base):

    # Notes
    #
    def edit_text_in_editor(self, text=None, editor=None):
        _, f = tempfile.mkstemp()

        # Write notes in tmp
        if text:
            with open(f, 'w') as tmpf:
                tmpf.write(text)

        if editor:
            # @fixme Use custom editor command
            cmd_str = editor.replace('%', f)
            subprocess.call(shlex.split(cmd_str))
        else:
            subprocess.call(['vim', f, '-c', 'startinsert'])  # '-u', 'NONE',

        with open(f, 'r') as file:
            text = file.read()

        return text

    # Notes
    #
    def success_note_created(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.success(s)

    def success_document_saved(self, doc):
        self.success("Document `%s` saved" % doc.name)

    def success_document_modified(self, doc, old_name, desc_mod):
        if old_name:
            if desc_mod:
                s = "Document `%s` renamed to `%s` and modified" % (old_name, doc.name)
            else:
                s = "Document `%s` renamed to `%s`" % (old_name, doc.name)
        else:
            if desc_mod:
                s = "Document `%s` modified" % doc.name
        self.success(s)

    def success_notes_deleted(self, n):
        notes = 'note' if n == 1 else 'notes'
        self.success("%i %s deleted" % (n, notes))

    def error_note_is_not_original(self, note):
        self.invalid("Note `%s` isn't original" % note.id)

    def error_note_not_found(self, note_id):
        self.not_found("Note %s doesn't exist" % note_id)


    # Documents
    #
    def success_document_created(self, doc):
        self.success("Created document `%s`" % doc.name)
        sys.exit(SUCCESS)

    #   success_document_modified

    def success_document_deleted(self, doc):
        self.success("Document `%s` deleted" % doc.name)

    def error_document_already_exists(self, name):
        self.already_exists("The document `%s` already exists" % name)

    def error_invalid_document_name(self, name):
        self.invalid("Invalid document name: %s" % name)

    def error_document_not_found(self, id):
        self.not_found("Document `%s` doesn't exist" % id)

    def error_invalid_document_name_or_id(self, name_or_id):
        self.not_found("Invalid document name or id: %s" % name_or_id)


    def find_note_by_id_or_error(self, note_id):
        q = Note.objects.filter(id=note_id)
        if q.count():
            return q.first()
        else:
            self.error_note_not_found(note_id)

    def find_document_by_id_or_error(self, doc_id):
        q = Document.objects.get(id=doc_id)
        if q.count():
            return q.first()
        else:
            self.error_document_not_found(doc_id)

    def find_document_by_name_or_error(self, name):
        q = Document.objects.get(name=name)
        if q.count():
            return q.first()
        else:
            self.error_document_not_found(name)

    def find_document_by_name_or_id_or_error(self, name_or_id):
        name_or_id = str(name_or_id)
        if re.match(r'^[0-9]+$', name_or_id):
            q = {'id': int(name_or_id)}
        elif DOCNAME_re.match(str(name_or_id)):
            q = {'name': name_or_id}
        else:
            self.error_invalid_document_name_or_id(name_or_id)

        try:
            return Document.objects.get(**q)
        except:
            self.error_document_not_found(name_or_id)


    def check_note_is_original(self, note):
        if not note.original:
            self.error_note_is_not_original(note)

    def check_document_name_is_valid(self, name):
        if not DOCNAME_re.match(name):
            self.error_invalid_document_name(name)

    def check_document_name_does_not_exist(self, name):
        try:
            # @fixme Direct use of the model object
            Document.objects.get(user_id=1, name=name)
        except:
            return
        self.error_document_already_exists(name)

    def get_note_attribute(self, note, attr):
        if attr == 'text':
            return note.text

    def filter_notes(self, filters):
        q = self.filter_query(filters)
        return Note.objects.filter(**q)

    # @todo Move to _functions.py
    #
    def filter_query(self, filters):
        ids, proj_name_or_id = set(), None

        # Default virtual tags
        vtags = {
            'ORIGINAL': True,
        }

        for f in filters:
            if IDS_re.match(f):
                ids.update(int(i) for i in f.split(','))
                continue

            m = PROJ_re.match(f)
            if m:
                proj_name_or_id = m.group(1)
                continue

            m = VTAG_re.match(f)
            if m:
                sign, vtag = m.group(1), m.group(2)
                if vtag in VTAGS:
                    vtags[vtag] = True if sign == '+' else False
                else:
                    self.cmd.stderr.write(self.cmd.style.ERROR("Unknown virtual tag `%s`" % vtag))
                    exit(1)

        q = {}
        if ids: q['id__in'] = list(ids)

        if proj_name_or_id:
            q['project'] = self.find_project_by_name_or_id_or_error(proj_name_or_id)

        if 'ORIGINAL' in vtags:
            q['original'] = vtags['ORIGINAL']

        if 'DOCUMENT' in vtags:
            q['documents__isnull'] = not vtags['DOCUMENT']

        return q


    # @fixme This is a helper
    #
    def create_document(self, name, note, desc=None, file=None):
        doc = Document(user_id=1, name=name, note=note, description=desc, file=file)
        doc.save()
        return doc

    def merge_notes(self, notes, proj, editor=None, quick=False):
        text = "\n\n".join(note.text.strip() for note in notes)

        if not quick:
            text = self.edit_text_in_editor(text, editor=editor)

        if text:
            return merge_notes(proj, text, notes)
        else:
            return None

    def synchronize_document(self, doc):
        if doc.file:
            if os.path.isfile(doc.file):
                timestamp = int(os.path.getmtime(doc.file))
            else:
                timestamp = 0

            mtime = pytz.utc.localize(datetime.datetime.fromtimestamp(timestamp))
            doc_modified = doc.note.modified.replace(microsecond=0)

            if doc_modified != mtime:
                if doc_modified > mtime:
                    with open(doc.file, 'w') as f:
                        f.write(doc.note.text)

                    from time import mktime
                    doc_ctime = mktime(doc.created.utctimetuple())
                    doc_mtime = mktime(doc.note.modified.utctimetuple())
                    os.utime(doc.file, times=(doc_ctime, doc_mtime))

                    sys.stdout.write("File synchronized.\n")
                else:
                    with open(doc.file, 'r') as f:
                        doc.note.modify_text(f.read(), time=mtime)
                    sys.stdout.write("Document synchronized.\n")

    def absolute_path(self, path):
        return os.path.abspath(os.path.expanduser(path))
