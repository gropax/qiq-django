from core.cli.management.module_tasks import module_tasks
from core.cli.management.module_tasks import ModuleTasks as BaseModuleTasks
from lexical_units.models import LexicalUnit
from languages.models import Language


@module_tasks
class ModuleTasks(BaseModuleTasks):
    def __init__(self):
        self.languages = Language.objects.all()
        super(ModuleTasks, self).__init__()

    def compute_tasks(self):
        for lang in self.languages:
            self.tasks[lang] = {name: tasks(lang) for name, tasks in self.__class__.model_tasks.items()}

    def get(self, names=[]):
        if names and len(names) >= 2:
            l = None
            for lang in self.languages:
                if names[0] == lang.code:
                    l = lang

            if l:
                for name, model_tasks in self.tasks[l].items():
                    if names[1] == name:
                        return model_tasks.get(names[2:])

            return None
        else:
            return self

    def types(self):
        cls = self.__class__
        task_names = sorted(cls.model_tasks.keys())
        langs = sorted(list(self.languages), key=lambda l: l.code)

        types = []
        for lang in langs:
            for name in task_names:
                model_tasks = cls.model_tasks[name]

                for name, *rest in self.tasks[lang][name].types():
                    newname = lang.code + '.' + name
                    types.append(tuple([newname] + rest))

        return types

    def by_task(self):
        for lang in self.languages:
            for tasks in self.tasks[lang].values():
                for task in tasks.by_task():
                    yield task

    def by_model(self):
        for lang in self.languages:
            for tasks in self.tasks[lang].values():
                for task in tasks.by_model():
                    yield task
