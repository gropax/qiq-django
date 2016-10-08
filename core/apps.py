from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    # Import cli module only after django initialization to access model layer
    def ready(self):
        import core.cli
