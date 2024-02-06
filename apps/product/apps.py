"""
Module: apps.py.

This module contains the app configuration for the product app.
"""

from django.apps import AppConfig


class ProductConfig(AppConfig):
    """Class contains the app configuration for the product app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.product"

    def ready(self):
        """
        Import signals from the product app.
        """
        import apps.product.signals  # noqa F401
