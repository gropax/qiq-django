from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand
import core.cli.format as f


@command('list', NoteCommand)
class ListCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='*', type=str,
                            help='filters used to select the notes')

    def action(self, args):
        notes = self.filter_notes(args.filters).all()

        if not notes:
            self.error_no_match()

        output = self.format(notes)
        self.stdout.write(output)

    def format(self, notes):
        headers = ['ID', 'Age', 'Project', 'Documents', 'Og', 'Rk', 'Text']
        table = f.list_table(headers, notes, self.list_row_data)
        return table.format()

    def list_row_data(self, note):
        return [
            note.id,
            f.format_age(note.created),
            f.format_project_name(note.project),
            f.format_document_list(note),
            f.format_original(note),
            note.rank,
            f.format_text(note),
        ]
