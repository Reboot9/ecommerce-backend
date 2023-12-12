"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.

"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import CustomUser
from apps.accounts.forms import CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Configuration for the Django admin interface for the CustomUser model.
    """

    add_form = CustomUserCreationForm
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("groups",)
    list_filter = ("is_active", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups")}),
        ("Important dates", {"fields": ("last_login",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    # fields displayed on User creation
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
