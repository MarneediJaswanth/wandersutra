from django.apps import AppConfig


class TravelAiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travel_ai"
    verbose_name = "India 360° Travel AI"

    def ready(self):
        # Pre-warm the engine and dataset on startup
        try:
            from .ai_engine import get_df, get_engine
            get_df()
            get_engine()
        except Exception:
            pass
