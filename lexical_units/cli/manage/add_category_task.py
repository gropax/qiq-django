from lexical_units.models import LexicalUnit
from .lexical_unit_tasks import LexicalUnitTasks
from core.cli.management.field_task import FieldTask, field_task


@field_task('cat', LexicalUnitTasks)
class AddCategoryTask(FieldTask):
    description = "Add grammatical category"

    @classmethod
    def check(cls, unit):
        if not unit.category:
            return cls(unit)


    def __init__(self, unit):
        self.lexical_unit = unit

    def perform(self):
        while True:
            cat = input("Enter a grammatical category for `%s` (pass) " % self.lexical_unit.lemma)
            if cat:
                if cat in LexicalUnit.CATEGORIES:
                    self.lexical_unit.grammatical_category = cat
                    self.lexical_unit.save()
                else:
                    print("Invalid category `%s` (choices: %s)" % (cat, ",".join(LexicalUnit.CATEGORIES)))
