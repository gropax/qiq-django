from core.cli.command import Command, command
from notes.cli.utils import Utils
from projects.cli.commands.project import ProjectCommand


@command('merge', ProjectCommand)
class MergeCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('name_or_id', type=str,
                            help='the name or ID of the project (fully qualified)')
        parser.add_argument('-e', '--editor', type=str,
                                default=self.config().get('editor'),
                                help='the command used to open the editor')
        parser.add_argument('-q', '--quick-merge', action='store_true',
                                help='merge notes without editing')

    def action(self, args):
        name_or_id = args.name_or_id
        proj = self.find_project_by_name_or_id_or_error(name_or_id)
        notes = proj.notes.filter(original=True)

        if notes.count() <= 1:
            self.warning_nothing_to_do()

        note = self.merge_notes(notes.all(), proj, editor=args.editor, quick=args.quick_merge)
        if note:
            self.success_project_notes_merged(note)
        else:
            self.warning_nothing_to_do()

    def success_project_notes_merged(self, note):
        self.success("Project's notes merges into note `%i`" % note.id)
