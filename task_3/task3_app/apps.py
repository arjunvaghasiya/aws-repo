from django.apps import AppConfig


class Task3AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task3_app'
    def ready(self):
        import task3_app.signals