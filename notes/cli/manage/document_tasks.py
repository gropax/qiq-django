from core.cli.management.model_tasks import model_tasks, ModelTasks
from .module_tasks import ModuleTasks
from notes.models import Document


@model_tasks('documents', ModuleTasks)
class DocumentTasks(ModelTasks):
    def models(self):
        return Document.objects.filter(user_id=1).all()
