"""
Module: apps.py.

This module contains the app configuration for the order app.
"""

from django.apps import AppConfig


class OrderConfig(AppConfig):
    """Class contains the app configuration for the order app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.order"
