from cli.management.commands._subcommand import Subcommand
import termblocks as tb
import cli.format as f


class InfoCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')

    def execute(self, args, options):
        note = self.find_note_by_id_or_error(options['id'])

        output = self.format(note)
        self.cmd.stdout.write(output)

    def format(self, note):
        table = f.model_table([
            ['ID', note.id],
            ['Username', note.user.username],
            ['Project', f.format_project_name(note.project)],
            ['Original', f.format_original(note)],
            ['Documents', f.format_document_list(note)],
            ['Created', f.format_creation_date(note)],
            ['Virtual tags', f.format_virtual_tags(note)],
            ['Previous notes', f.format_references(note.references)],
            ['Next notes', f.format_references(note.referencers)],
            ['Rank', note.rank],
        ])
        text = tb.TextBlock(note.text)
        margin = tb.MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = tb.VerticalLayout([table, margin])

        return vlayout.format()
