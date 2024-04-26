"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.

"""
from typing import Union, Tuple, List

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import CustomUserCreationForm
from apps.accounts.models import CustomUser
from apps.base.admin import toggle_is_active


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Configuration for the Django admin interface for the CustomUser model.
    """

    add_form = CustomUserCreationForm
    list_display = [
        "shortened_email",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = [
        "groups",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    actions = [toggle_is_active]
    list_editable = [
        "is_active",
    ]

    def get_readonly_fields(self, request, obj=None) -> Union[Tuple[str, ...], List[str]]:
        """
        Determine the list of fields that should be read-only in the admin interface.

        :param request: HTTP request to be processed
        :param obj: instance to be edited by admin
        :return: a tuple or list of field names to be marked as read_only
        """
        # Make email read-only when editing an existing user
        if obj:
            return super().get_readonly_fields(request, obj) + ("email",)
        # Allow changing email when creating a new user
        return super().get_readonly_fields(request, obj)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser", "groups")}),
        (_("Important dates"), {"fields": ("last_login",)}),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # fields displayed on User creation
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )

    def shortened_email(self, obj):
        """
        Method to display a shortened version of the email address.
        """
        username, domain = obj.email.split("@")
        truncated_username = username[:16] + "..." if len(username) > 23 else username
        return f"{truncated_username}@{domain}"
