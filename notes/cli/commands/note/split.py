from core.cli.command import Command, command
from notes.cli.utils import Utils
from notes.cli.commands.note import NoteCommand
from notes.models import Note
from notes.helpers import merge_notes
from math import ceil
import difflib


@command('split', NoteCommand)
class SplitCommand(Command, Utils):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='the ID of the note')
        parser.add_argument('-e', '--editor', type=str,
                                default=self.config().get('editor'),
                                help='the command used to open the editor')

        proj_grp = parser.add_mutually_exclusive_group()
        proj_grp.add_argument('-p', '--project', type=str,
                                help='the project in which to store the note')
        proj_grp.add_argument('-P', '--no-project', action='store_true', default=False,
                                help='do not store the note in any project')
        parser.add_argument('-c', '--create-project', action='store_true', default=False,
                                help='create the project if it doesn\'t exist')

    def execute(self, args):
        note = self.find_note_by_id_or_error(args.id)
        if args.no_project:
            proj = None
        else:
            proj = self.get_or_prompt_project(project=args.project,
                                              create_project=args.create_project,
                                              default=note.project)

        f = self.edit_note_in_editor(text=note.text, editor=args.editor)

        with open(f, 'r') as file:
            keep_text = file.read()

        if keep_text:
            keep, new = self.split_note(proj, note, keep_text)
            self.success_note_split(note, keep, new)
        else:
            self.warning_nothing_to_do()

    def success_note_split(self, old, keep, new):
        self.success("Split note %i into notes %i and %i" % (old.id, keep.id, new.id))

    def split_note(self, proj, note, keep_text):
        # Compute new note's text
        new_text = ""
        for s in difflib.ndiff(note.text, keep_text):
            if s[0] == '-':
                new_text += s[-1]

        # Compute the rank of the notes
        keep_rank = ceil(note.rank * len(keep_text) / len(note.text))
        new_rank = max(note.rank - keep_rank, 1)

        # Create the now notes
        keep_note = Note(user_id=1, project=note.project, text=keep_text, rank=keep_rank)
        keep_note.save()
        new_note = Note(user_id=1, project=proj, text=new_text, rank=new_rank)
        new_note.save()

        # Create references with the previous note
        note.referencers.add(keep_note, new_note)

        # Remove original flag on old note
        note.original = False
        note.save()

        # Update reference of documents to the keep note
        docs = [d for d in note.documents.all()]
        for doc in docs:
            doc.note = keep_note
            doc.save()

        return keep_note, new_note
