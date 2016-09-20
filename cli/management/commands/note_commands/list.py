from cli.management.commands._subcommand import Subcommand
import cli.format as f


class ListCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='*', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        notes = self.filter_notes(options['filters']).all()

        if not notes:
            self.error_no_match()

        output = self.format(notes)
        self.cmd.stdout.write(output)

    def format(self, notes):
        headers = ['ID', 'Age', 'Project', 'Documents', 'Og', 'Rk', 'Text']
        table = f.list_table(headers, notes, self.list_row_data)
        return table.format()

    def list_row_data(self, note):
        return [
            note.id,
            note.age(),
            f.format_project_name(note.project),
            f.format_document_list(note),
            f.format_original(note),
            note.rank,
            f.format_text(note),
        ]
