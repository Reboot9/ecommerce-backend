"""
Module: models.py.

This module contains the base models used throughout the application.
"""
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseID(models.Model):
    """Model to define UUID as primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True


class BaseDate(models.Model):
    """Add additional fields for creation and update dates."""

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True
