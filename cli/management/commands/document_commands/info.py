from cli.management.commands._subcommand import Subcommand
import termblocks as tb
import cli.format as f


class InfoCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str, help='the name or the id of the document')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        doc = self.find_document_by_name_or_id_or_error(name_or_id)

        output = self.format(doc)
        self.cmd.stdout.write(output)

    def format(self, doc):
        note = doc.note
        table = f.model_table([
            ['ID', doc.id],
            ['Username', note.user.username],
            ['Project', f.format_project_name(note.project)],
            ['Name', doc.name],
            ['Created', f.format_creation_date(doc)],
            ['Rank', note.rank],
        ])
        text = tb.TextBlock(note.text)
        margin = tb.MarginBlock(text, left=4, right=4, top=1, bottom=1)
        vlayout = tb.VerticalLayout([table, margin])

        return vlayout.format()
