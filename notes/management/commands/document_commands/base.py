import sys
import re
from notes.models import Document, Note
from notes.management.commands._subcommand import Subcommand


# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

class DocumentCommand(Subcommand):
    def success_document_modified(self, doc):
        s = "Modified document `%s`" % doc.name
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def error_document_not_found(self, id):
        s = "Document `%s` doesn't exist" % id
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        sys.exit(32)

    def error_note_is_not_original(self, note):
        s = "Note `%s` isn't original" % note.id
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        sys.exit(32)

    def exit_invalid_document_name(self, name):
        s = "Invalid document name: %s" % name
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        sys.exit(30)

    def exit_invalid_document_name_or_id(self, name_or_id):
        s = "Invalid document name or id: %s" % name_or_id
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        sys.exit(30)

    def exit_document_already_exists(self, name):
        s = "The document `%s` already exists" % name
        self.cmd.stdout.write(self.cmd.style.ERROR(s))
        sys.exit(31)

    def check_note_is_original(self, note):
        if not note.original:
            self.error_note_is_not_original(note)

    def check_document_name_is_valid(self, name):
        if not DOCNAME_re.match(name):
            self.exit_invalid_document_name(name)

    def check_document_name_does_not_exist(self, name):
        try:
            Document.objects.get(user_id=1, name=name)
        except:
            return
        self.exit_document_already_exists(name)

    def find_document_by_id_or_error(self, doc_id):
        try:
            return Document.objects.get(id=doc_id)
        except:
            self.error_document_not_found(doc_id)

    def find_document_by_name_or_error(self, name):
        try:
            return Document.objects.get(name=name)
        except:
            self.error_document_not_found(name)

    def find_document_by_name_or_id_or_error(self, name_or_id):
        name_or_id = str(name_or_id)
        try:
            if re.match(r'^[0-9]+$', name_or_id):
                doc_id = int(name_or_id)
                return Document.objects.get(id=doc_id)
            elif DOCNAME_re.match(str(name_or_id)):
                name = name_or_id
                return Document.objects.get(name=name)
            else:
                self.error_invalid_document_name_or_id(name_or_id)
        except:
            self.error_document_not_found(name_or_id)

    def get_note_or_exit(self, note_id):
        try:
            return Note.objects.get(id=note_id)
        except:
            self.notify_note_not_found(note_id)
            sys.exit(1)

    def notify_created(self, doc):
        s = 'Created document `%s`' % doc.name
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def create_document(self, name, note, desc=None):
        doc = Document(user_id=1, name=name, note=note, description=desc)
        doc.save()
        return doc
