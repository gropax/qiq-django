from .project_tasks import ProjectTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('desc', ProjectTasks)
class AddDescription(FieldTask):
    description = "Complete project's description"

    @classmethod
    def check(cls, proj):
        if not proj.description:
            return cls(proj)


    def __init__(self, proj):
        self.project = proj

    def perform(self):
        # @fixme interactions
        desc = input("Enter a description for `%s`  (pass) " % self.project.full_name())
        if desc:
            self.project.description = desc
            self.project.save()
