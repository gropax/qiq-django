import re
import tempfile
import subprocess
import shlex
import cli.utils.projects as prj
from projects.cli.utils import Utils as Base
from notes.models import Note, Document

# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

VTAGS = ['ORIGINAL', 'DOCUMENT']

IDS_re = re.compile(r'^\d+(?:,\d+)*$')
PROJ_re = re.compile(r'^proj(?:ect)?:([a-z]+(?:\/[a-z]+)*)$')
VTAG_re = re.compile(r'^(\+|-)([A-Z]+)$')


class Utils(Base):

    # Notes
    #
    def edit_note_in_editor(self, args, text=None):
        _, f = tempfile.mkstemp()

        # Write notes in tmp
        if text:
            with open(f, 'w') as tmpf:
                tmpf.write(text)

        if args.editor:
            # @fixme Use custom editor command
            cmd_str = args.editor.replace('%', f)
            subprocess.call(shlex.split(cmd_str))
        else:
            subprocess.call(['vim', f, '-c', 'startinsert'])  # '-u', 'NONE',

        return f

    # Notes
    #
    def success_note_created(self, note):
        s = 'Created note %s' % note.id
        if note.project:
            s += " in %s" % note.project.full_name()
        self.success(s)

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


    def filter_notes(self, filters):
        q = self.filter_query(filters)
        return Note.objects.filter(**q)

    # @todo Move to _functions.py
    #
    def filter_query(self, filters):
        ids, proj_name, vtags = set(), None, {}

        for f in filters:
            if IDS_re.match(f):
                ids.update(int(i) for i in f.split(','))
                continue

            m = PROJ_re.match(f)
            if m:
                proj_name = m.group(1)
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

        if proj_name:
            #proj = prj.get_project(proj_name)
            proj = prj.get_by_fullname(proj_name)
            if proj:
                q['project'] = proj
            else:
                self.cmd.stderr.write(self.cmd.style.ERROR("Unknown project `%s`" % proj_name))
                exit(1)

        if 'ORIGINAL' in vtags:
            q['original'] = vtags['ORIGINAL']

        if 'DOCUMENT' in vtags:
            q['documents__isnull'] = not vtags['DOCUMENT']

        return q


    # @fixme This is a helper
    #
    def create_document(self, name, note, desc=None):
        doc = Document(user_id=1, name=name, note=note, description=desc)
        doc.save()
        return doc

