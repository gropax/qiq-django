from django.apps import AppConfig


class LexicalUnitsConfig(AppConfig):
    name = 'lexical_units'

    # Import cli module only after django initialization to access model layer
    def ready(self):
        import lexical_units.cli
