from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    # Import cli module only after django initialization to access model layer
    def ready(self):
        import projects.cli
