import sys
from notes.models import Document
from .base import DocumentCommand


class ModifyCommand(DocumentCommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the document')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the document')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        old_name, desc_mod = None, None

        new_name = options['new_name']
        if new_name and new_name != doc.name:
            old_name = doc.name
            doc.name = new_name

        desc = options['description']
        if desc and desc != doc.description:
            desc_mod = True
            doc.description = desc

        if old_name or desc_mod:
            doc.save()
            self.success_document_modified(doc, old_name, desc_mod)
        else:
            self.warning_nothing_to_do()

    def success_document_modified(self, doc, old_name, desc_mod):
        if old_name:
            if desc_mod:
                s = "Document `%s` renamed to `%s` and modified" % (old_name, doc.name)
            else:
                s = "Document `%s` renamed to `%s`" % (old_name, doc.name)
        else:
            if desc_mod:
                s = "Document `%s` modified" % doc.name
        self.cmd.stdout.write(self.cmd.style.SUCCESS(s))

    def warning_nothing_to_do(self):
        s = "Nothing to do"
        self.cmd.stdout.write(self.cmd.style.WARNING(s))
        sys.exit()
