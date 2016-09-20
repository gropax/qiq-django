from cli.management.commands._subcommand import Subcommand


class DeleteCommand(Subcommand):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')

    def execute(self, args, options):
        notes = self.filter_notes(options['filters'])

        no, _ = notes.delete()
        if no:
            self.success_notes_deleted(no)
        else:
            self.error_no_match()
