"""
Contains configurations for the warehouse app.
"""
from django.apps import AppConfig


class WarehouseConfig(AppConfig):
    """Class contains the app configuration for the warehouse app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.warehouse"
