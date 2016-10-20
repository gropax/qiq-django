from core.cli.management.module_tasks import module_tasks
from core.cli.management.module_tasks import ModuleTasks as BaseModuleTasks
from notes.models import Note


@module_tasks
class ModuleTasks(BaseModuleTasks):
    pass
