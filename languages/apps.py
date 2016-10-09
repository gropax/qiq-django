from django.apps import AppConfig


class LanguagesConfig(AppConfig):
    name = 'languages'

    # Import cli module only after django initialization to access model layer
    def ready(self):
        import languages.cli
