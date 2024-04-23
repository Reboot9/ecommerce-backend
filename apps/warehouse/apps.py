"""
Contains configurations for the warehouse app.
"""
from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    """Class contains the app configuration for the warehouse app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.warehouse"

    def ready(self):
        """Method called when the app is ready. Connects signals, related to Warehouse."""
        import apps.warehouse.signals  # noqa: F401
