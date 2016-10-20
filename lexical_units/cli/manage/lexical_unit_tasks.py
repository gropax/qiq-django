from core.cli.management.model_tasks import model_tasks, ModelTasks
from .module_tasks import ModuleTasks
from lexical_units.models import LexicalUnit


@model_tasks('units', ModuleTasks)
class LexicalUnitTasks(ModelTasks):
    def __init__(self, lang):
        self.language = lang
        super(LexicalUnitTasks, self).__init__()

    def models(self):
        return LexicalUnit.objects.filter(user_id=1).all()
        #return LexicalUnit.objects.filter(user_id=1, language=self.language).all()

    #def types(self):
        #print("tasks_by_class: %s" % self.tasks_by_class)
        #super(LexicalUnitTasks, self).types()
