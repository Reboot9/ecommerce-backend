"""
Contains configurations for the payment app.
"""
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    """Class contains the app configuration for the payment app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payment"
