"""
Forms for user creation and modification.
"""
from typing import Dict, Type

from django.contrib.auth.forms import UserCreationForm
from django import forms

from apps.accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user creation, extending Django's UserCreationForm.

    This form includes customizations such as password confirmation.
    """

    password1 = forms.CharField(
        label="Password",
        strip=False,
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields: tuple = ("email", "password1", "password2")
        field_classes: Dict[str, Type[forms.Field]] = {
            "email": forms.EmailField,
            "password1": forms.PasswordInput,
            "password2": forms.PasswordInput,
        }
