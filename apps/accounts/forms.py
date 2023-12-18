"""
Forms for user creation and modification.
"""
import re
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
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )
    is_superuser = forms.BooleanField(
        label="Is Superuser",
        required=False,
        help_text="Check this box if the user should have superuser privileges.",
    )
    is_staff = forms.BooleanField(
        label="Is Staff",
        required=False,
        help_text="Check this box if the user should have staff privileges.",
    )

    class Meta:
        model = CustomUser
        fields: tuple = ("email", "password1", "password2", "is_superuser", "is_staff")
        field_classes: Dict[str, Type[forms.Field]] = {
            "email": forms.EmailField,
            "password1": forms.PasswordInput,
            "password2": forms.PasswordInput,
        }

    def clean_password1(self):
        """
        Clean and validate the 'password1' field.

        This method ensures that the provided password contains only Latin letters,
        numbers, and the specified special characters (@#$%^&+=). If the password
        contains any other characters, a ValidationError is raised.

        :return: cleaned and validated password1
        """
        password1 = self.cleaned_data.get("password1")

        if not re.match("^[a-zA-Z0-9@#$%^&+=]+$", password1):
            raise forms.ValidationError(
                "Password must contain only Latin letters,"
                " numbers, and special characters (@#$%^&+=)."
            )
        return password1
