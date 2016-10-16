from core.cli.management.model_tasks import model_tasks, ModelTasks
from .module_tasks import ModuleTasks
from projects.models import Project


@model_tasks('projects', ModuleTasks)
class ProjectTasks(ModelTasks):
    @classmethod
    def models(cls):
        projs = Project.objects.filter(user_id=1).all()
        return sorted(projs, key=lambda p: p.full_name())
