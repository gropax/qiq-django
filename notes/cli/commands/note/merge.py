from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand
from notes.helpers import merge_notes


@command('merge', NoteCommand)
class MergeCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('filters', nargs='+', type=str,
                            help='filters used to select the notes')
        parser.add_argument('-e', '--editor', type=str,
                                default=self.config().get('editor'),
                                help='the command used to open the editor')
        parser.add_argument('-q', '--quick-merge', action='store_true',
                                help='merge notes without editing')

        proj_grp = parser.add_mutually_exclusive_group()
        proj_grp.add_argument('-p', '--project', type=str,
                                help='the project in which to store the note')
        proj_grp.add_argument('-P', '--no-project', action='store_true', default=False,
                                help='do not store the note in any project')
        parser.add_argument('-c', '--create-project', action='store_true', default=False,
                                help='create the project if it doesn\'t exist')

    def action(self, args):
        notes = self.filter_notes(args.filters).all()

        if not notes:
            self.error_no_match()

        proj = self.get_or_prompt_project(args, default=self.default_project(notes))

        text = "\n\n".join(note.text.strip() for note in notes)

        if not args.quick_merge:
            f = self.edit_note_in_editor(args, text=text)
            with open(f, 'r') as file:
                text = file.read()

        if text:
            note = merge_notes(proj, text, notes)
            self.success_note_created(note)
        else:
            self.warning_nothing_to_do()

    def default_project(self, notes):
        for note in notes:
            if note.project:
                return note.project
        return None
