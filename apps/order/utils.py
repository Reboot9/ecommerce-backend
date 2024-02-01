"""
Module: phone_validators.

This module contains a Django validator for phone numbers.
"""
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_validator = RegexValidator(
    regex=r"^\+\d{2}\(\d{3}\)\d{3}-\d{2}-\d{2}$",
    message=_(
        "Phone number must be entered in the format: '+38(050)111-11-11'. Up to 17 digits allowed."
    ),
)
