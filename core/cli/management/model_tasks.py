def model_tasks(name, module_tasks):
    def decorator(cls):
        if not hasattr(module_tasks, 'model_tasks'):
            module_tasks.model_tasks = {}

        module_tasks.model_tasks[name] = cls
        cls.name = name

        return cls

    return decorator


class ModelTasks(object):
    def __init__(self):
        self.tasks_by_class = {}
        self.tasks_by_model = {}
        self.model_count = 0

        self.compute_tasks()

    def compute_tasks(self):
        cls = self.__class__

        self.tasks_by_class = {ft: [] for _, ft in cls.field_tasks.items()}

        for model in self.models():
            self.model_count += 1

            for name, ft in cls.field_tasks.items():
                if not model in self.tasks_by_model:
                    self.tasks_by_model[model] = []

                task = ft.check(model)
                if task:
                    self.tasks_by_class[ft].append(task)
                    self.tasks_by_model[model].append(task)

    def get(self, names=[]):
        if names:
            if len(names) == 1:
                for name, field_tasks in self.__class__.field_tasks.items():
                    if names[0] == name:
                        return self.tasks_by_class[field_tasks]
            return None
        else:
            return self

    def types(self):
        cls = self.__class__
        task_names = sorted(cls.field_tasks.keys())

        types = []
        for name in task_names:
            task_type = cls.field_tasks[name]

            nb = len(self.tasks_by_class[task_type])
            comp = (self.model_count - nb) / self.model_count if self.model_count else 0
            types.append((self.name + '.' + name, task_type, nb, comp))

        return types

    def by_task(self):
        for cls, tasks in self.tasks_by_class.items():
            for task in tasks:
                yield task

    def by_model(self):
        for model, tasks in self.tasks_by_model.items():
            for task in tasks:
                yield task
