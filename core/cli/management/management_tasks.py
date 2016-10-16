class ManagementTasks(object):
    module_tasks = []

    def __init__(self):
        self.tasks = [cls() for cls in self.__class__.module_tasks]

    def get(self, names):
        for module_tasks in self.tasks:
            tasks = module_tasks.get(names)
            if tasks:
                return tasks
        return None

    def types(self):
        types = []
        for module_tasks in self.tasks:
            types += module_tasks.types()
        return types

    def by_task(self):
        for tasks in self.tasks:
            for task in tasks.by_task():
                yield task

    def by_model(self):
        for tasks in self.tasks:
            for task in tasks.by_model():
                yield task
