from core.cli.management.module_tasks import module_tasks
from core.cli.management.module_tasks import ModuleTasks as BaseModuleTasks
from projects.models import Project


@module_tasks
class ModuleTasks(BaseModuleTasks):
    def task_types(self):
        for model_name, model_tasks in self.model_tasks_by_name.items():
            for task_name, tasks in model_tasks.tasks_by_type():
                name = ".".join([model_name, task_name])
                nb = len(tasks)
                comp = nb / model_tasks.data_count[task_name]
                desc = model_tasks.__class__.field_tasks[task_name].description
                yield (name, nb, comp, desc)
