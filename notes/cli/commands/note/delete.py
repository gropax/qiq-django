from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand


@command('delete', NoteCommand)
class DeleteCommand(Command, Utils):
    aliases = ('del',)

    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')

    def action(self, args):
        notes = self.filter_notes(args.filters)

        no, _ = notes.delete()
        if no:
            self.success_notes_deleted(no)
        else:
            self.error_no_match()
