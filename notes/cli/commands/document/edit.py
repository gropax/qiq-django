from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.document import DocumentCommand


@command('edit', DocumentCommand)
class EditCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or the id of the document')
        parser.add_argument('-e', '--editor', type=str,
                                default=self.config().get('editor'),
                                help='the command used to open the editor')

    def action(self, args):
        name_or_id = args.name_or_id
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        note = self.merge_notes([doc.note], doc.note.project, editor=args.editor)
        if note:
            self.success_document_saved(doc)
        else:
            self.warning_nothing_to_do()
