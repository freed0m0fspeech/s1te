from django.apps import AppConfig


class FreedomOfSpeechConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "freedom_of_speech"

    # def ready(self):
    #     from jobs import updater
    #     updater.start()
