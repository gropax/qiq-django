import os
from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.document import DocumentCommand


@command('modify', DocumentCommand)
class ModifyCommand(Command, Utils):
    aliases = ('mod',)

    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')
        parser.add_argument('-d', '--description', type=str,
                            help='the description of the document')
        parser.add_argument('-n', '--new-name', type=str,
                            help='the new name of the document')
        parser.add_argument('-f', '--file', type=str,
                            help='synchronize document with file')

    def action(self, args):
        name_or_id = args.name_or_id
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        old_name, desc_mod, file_mod = None, None, None

        new_name = args.new_name
        if new_name and new_name != doc.name:
            self.check_document_name_is_valid(new_name)
            old_name = doc.name
            doc.name = new_name

        desc = args.description
        if desc and desc != doc.description:
            desc_mod = True
            doc.description = desc

        f = None
        if args.file:
            f = self.absolute_path(args.file)
            if f != doc.file:
                if os.path.isfile(f):
                    if not self.ask('File `%s` already exists. Synchronize it anyway ?' % f, default='no'):
                        self.warning_operation_aborted()

            file_mod = True
            doc.file = f
            self.synchronize_document(doc)

        if old_name or desc_mod or file_mod:
            doc.save()
            self.success_document_modified(doc, old_name, desc_mod or file_mod)
        else:
            self.warning_nothing_to_do()
