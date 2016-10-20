from .note_tasks import NoteTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('doc', NoteTasks)
class AddDocument(FieldTask):
    description = "Create a new document for a large note"

    @classmethod
    def check(cls, note):
        if note.rank > 50:
            return cls(proj)


    def __init__(self, note):
        self.note = note

    def perform(self):
        raise NotImplementedError()
