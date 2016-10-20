from .lexical_unit_tasks import LexicalUnitTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('fake', LexicalUnitTasks)
class FakeTask(FieldTask):
    description = "Fake"

    @classmethod
    def check(cls, unit):
        return cls(unit)


    def __init__(self, unit):
        self.lexical_unit = unit

    def perform(self):
        raise NotImplemented()
