from core.cli.management.model_tasks import model_tasks, ModelTasks
from .module_tasks import ModuleTasks
from notes.models import Note


@model_tasks('notes', ModuleTasks)
class NoteTasks(ModelTasks):
    def models(self):
        return Note.objects.filter(user_id=1).all()
