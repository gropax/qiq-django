from argparse import FileType
from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand
from notes.helpers import create_note
from notes.models import Note


@command('new', NoteCommand)
class NewCommand(Command, Utils):
    def add_arguments(self, parser):
        input_grp = parser.add_mutually_exclusive_group()
        input_grp.add_argument('-e', '--editor', type=str,
                                default=self.config().get('editor'),
                                help='the command used to open the editor')
        input_grp.add_argument('-f', '--infile', type=FileType('r'),
                                help='the file containing the text of the note')

        proj_grp = parser.add_mutually_exclusive_group()
        proj_grp.add_argument('-p', '--project', type=str,
                                help='the project in which to store the note')
        proj_grp.add_argument('-l', '--last-project', action='store_true', default=False,
                                help='use the same project as the latest note')
        proj_grp.add_argument('-P', '--no-project', action='store_true', default=False,
                                help='do not store the note in any project')
        parser.add_argument('-c', '--create-project', action='store_true', default=False,
                                help='create the project if it doesn\'t exist')

    def action(self, args):
        if args.last_project:
            last_note = Note.objects.filter(user_id=1, project__isnull=False) \
                                       .order_by('-created').first()
            proj = last_note.project
        elif args.no_project:
            proj = None
        else:
            proj = self.get_or_prompt_project(project=args.project,
                                              create_project=args.create_project)

        if args.infile:
            f = args.infile.name
            with open(f, 'r') as file:
                text = file.read()
        else:
            text = self.edit_text_in_editor(text=None, editor=args.editor)


        if text:
            note = create_note(proj, text)
            self.success_note_created(note)
        else:
            self.warning_nothing_to_do()
