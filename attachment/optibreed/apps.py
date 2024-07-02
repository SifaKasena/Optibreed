from django.apps import AppConfig


class OptibreedConfig(AppConfig):
    """
    AppConfig for the Optibreed app.

    This class represents the configuration for the Optibreed app in a Django project.
    It sets the default auto field to 'django.db.models.BigAutoField' and specifies the name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'optibreed'
