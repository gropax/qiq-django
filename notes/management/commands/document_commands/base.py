import sys
import re
from notes.models import Document, Note
from notes.management.commands._subcommand import Subcommand


# Document's name begin with a letter, may contain numbers and dots, cannot end
# with a dot. All letters are lower case.
DOCNAME_re = re.compile(r'^[a-z][a-z0-9]*(?:\.[a-z0-9]+)*$')

class DocumentCommand(Subcommand):

    ###########################
    # Terminal output methods #
    ###########################

    def success_document_created(self, doc):
        self.success("Created document `%s`" % doc.name)
        sys.exit(0)

    #   success_document_modified

    def success_document_deleted(self, doc):
        self.success("Document `%s` deleted" % doc.name)
        sys.exit(0)

    def error_document_not_found(self, id):
        self.error("Document `%s` doesn't exist" % id)
        sys.exit(32)

    def error_note_is_not_original(self, note):
        self.error("Note `%s` isn't original" % note.id)
        sys.exit(32)

    def error_invalid_document_name(self, name):
        self.error("Invalid document name: %s" % name)
        sys.exit(30)

    def error_invalid_document_name_or_id(self, name_or_id):
        self.error("Invalid document name or id: %s" % name_or_id)
        sys.exit(30)

    def error_document_already_exists(self, name):
        self.error("The document `%s` already exists" % name)
        sys.exit(31)


    #####################
    # Validation Guards #
    #####################

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


    ###############################
    # Find models or return error #
    ###############################

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


    # @fixme This is a helper
    #
    def create_document(self, name, note, desc=None):
        doc = Document(user_id=1, name=name, note=note, description=desc)
        doc.save()
        return doc

