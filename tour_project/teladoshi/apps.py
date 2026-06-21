from django.apps import AppConfig


class TeladoshiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "teladoshi"

    def ready(self) -> None:
        import teladoshi.signals.handlers  # noqa: F401
