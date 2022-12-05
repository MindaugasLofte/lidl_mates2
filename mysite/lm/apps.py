from django.apps import AppConfig


class LmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lm'
    def ready(self):
        from .signals import create_profile, save_profile