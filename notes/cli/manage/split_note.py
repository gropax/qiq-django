from .note_tasks import NoteTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('split', NoteTasks)
class SplitNote(FieldTask):
    description = "Split large notes"

    @classmethod
    def check(cls, note):
        if note.rank > 100:
            return cls(proj)


    def __init__(self, note):
        self.note = note

    def perform(self):
        raise NotImplementedError()
