from .management_tasks import ManagementTasks


def module_tasks(cls):
    ManagementTasks.module_tasks.append(cls)
    return cls


class ModuleTasks(object):
    def __init__(self):
        self.tasks = {name: tasks() for name, tasks in self.__class__.model_tasks.items()}

    def get(self, names=[]):
        if names:
            for name, model_tasks in self.tasks.items():
                if names[0] == name:
                    return model_tasks.get(names[1:])
            return None
        else:
            return self

    def types(self):
        return [tup for name, model_tasks in self.tasks.items()
                    for tup in model_tasks.types()]

    def by_task(self):
        for tasks in self.tasks.values():
            for task in tasks.by_task():
                yield task

    def by_model(self):
        for tasks in self.tasks.values():
            for task in tasks.by_model():
                yield task
