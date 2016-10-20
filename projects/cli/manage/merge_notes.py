from .project_tasks import ProjectTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('merge', ProjectTasks)
class MergeNotes(FieldTask):
    description = "Merge all notes in a project"

    @classmethod
    def check(cls, proj):
        if proj.notes.count() > 1:
            return cls(proj)


    def __init__(self, proj):
        self.project = proj

    def perform(self):
        raise NotImplementedError()
