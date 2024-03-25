"""
Module: apps.py.

This module contains the app configuration for the cart app.
"""
from django.apps import AppConfig


class CartConfig(AppConfig):
    """Class contains the app configuration for the cart app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cart"

    def ready(self):
        """Connects signals for the cart app."""
        import apps.cart.signals  # noqa: F401
