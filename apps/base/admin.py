"""
Admin related classes and function that can be used in any part of the project.
"""
from django.contrib import admin
from django.db.models import Case, When, Value


@admin.action(description="Toggle is_active status for selected entries")
def toggle_is_active(modeladmin, request, queryset):
    """
    Custom action to toggle is_active status of queryset.

    :param modeladmin: The ModelAdmin instance.
    :param request: The current HTTP request.
    :param queryset: The queryset containing the selected entries.
    :return: None because this function updates the queryset in place.
    """
    if queryset.model._meta.get_field("is_active"):
        updated_count = queryset.update(
            is_active=Case(
                When(is_active=True, then=Value(False)),
                default=Value(True),
            )
        )
        modeladmin.message_user(
            request,
            f"{updated_count} "
            f"{'entry was' if updated_count == 1 else 'entries were'} "
            f"toggled.",
            level="SUCCESS",
        )
    else:
        modeladmin.message_user(
            request,
            "This model does not have the 'is_active' field.",
            level="ERROR",
        )
