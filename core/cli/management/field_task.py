def field_task(name, model_tasks):
    def decorator(cls):
        if not hasattr(model_tasks, 'field_tasks'):
            model_tasks.field_tasks = {}
        model_tasks.field_tasks[name] = cls
        return cls
    return decorator


class FieldTask(object):
    description = "#DESCRIPTION"

    @classmethod
    def check(cls, proj):
        raise NotImplemented("FieldTask::check")


    def __init__(self, model):
        self.model = model

    def perform(self):
        raise NotImplemented("FieldTask#perform")
