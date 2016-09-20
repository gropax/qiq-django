from cli.management.commands._subcommand import Subcommand
import cli.format as f


class InfoCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')

    def execute(self, args, options):
        name_or_id = options['name_or_id']
        proj = self.find_project_by_name_or_id_or_error(name_or_id)

        output = self.format(proj)
        self.cmd.stdout.write(output)

    def format(self, proj):
        table = f.model_table([
            ['ID', proj.id],
            ['Name', f.format_project_name(proj)],
            ['Description', f.format_project_description(proj)],
            ['Original notes', f.format_project_note_no(proj.notes.filter(original=True).count())],
            ['Old notes', proj.notes.filter(original=False).count()],
        ])
        return table.format()
