from django.apps import AppConfig


class FootballConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.football"

    def ready(self):
        # for registry
        import demo.football.dashboards  # type: ignore # noqa
