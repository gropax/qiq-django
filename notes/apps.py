from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = 'notes'

    # Import cli module only after django initialization to access model layer
    def ready(self):
        import notes.cli
