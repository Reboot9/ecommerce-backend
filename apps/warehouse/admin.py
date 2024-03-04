"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.
"""
from django.contrib import admin

from django.db.models import Case, Value, When
from django.utils.translation import gettext_lazy as _

from apps.warehouse.models import (
    ConsignmentNote,
    Transaction,
    Reserve,
    Warehouse,
)


@admin.action(description="Toggle selected is_active status")
def toggle_is_active(modeladmin, request, queryset):
    """
    Custom action to toggle is_active status of queryset.

    :param modeladmin: The ModelAdmin instance.
    :param request: The current HTTP request.
    :param queryset: The queryset containing the selected entries.
    :return: None because this function updates the queryset in place.
    """
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


# class ConsignmentNoteInline(admin.StackedInline):
#     """
#     Inline for managing ConsignmentNote objects in the admin.
#     """
#
#     model = ConsignmentNote
#     fields = ("number", "consignment_date")
#     extra = 1
#     can_delete = False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin class for Goods Arrival model.
    """

    list_display = [
        "id",
        "get_consignment_number",
        "get_consignment_date",
        "transaction_type",
        "product",
        "product_category",
        "quantity",
        "comment",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "transaction_type",
        "consignment_note__consignment_date",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["product", "consignment_note"]
    search_fields = ["consignment_note.number", "comment"]
    search_help_text = "Search for consignment notes by number or comment"
    date_hierarchy = "consignment_note__consignment_date"  # Consider changing this field
    # inlines = [ConsignmentNoteInline, ]
    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "consignment_note",
                    "transaction_type",
                    "product",
                    "quantity",
                    "comment",
                )
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_consignment_number(self, obj) -> str:
        """
        Returns the consignment note number associated with the given object.
        """
        return obj.consignment_note.number if obj.consignment_note else None

    get_consignment_number.short_description = _("Consignment Note Number")

    def get_consignment_date(self, obj) -> str:
        """
        Returns the consignment note sign date associated with the given object.
        """
        return obj.consignment_note.consignment_date if obj.consignment_note else None

    get_consignment_date.short_description = _("Consignment Note Date")


@admin.register(ConsignmentNote)
class ConsignmentNoteAdmin(admin.ModelAdmin):
    """
    Admin class for Consignment Note model.
    """

    list_display = [
        "id",
        "number",
        "consignment_date",
        "created_at",
        "updated_at",
    ]
    list_filter = ["consignment_date", "created_at", "updated_at"]
    search_fields = ["number"]
    date_hierarchy = "consignment_date"
    search_help_text = _("Search for consignment notes by number")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "number",
                    "consignment_date",
                )
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    """
    Admin class for Reserve model.
    """

    list_display = [
        "id",
        "order",
        "reserved_item",
        "quantity",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = [
        "reserved_item",
    ]
    search_fields = ["order__order_number", "reserved_item__name"]
    search_help_text = _("Search for reservations by order and reserved item name")
    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("order", "reserved_item", "quantity")}),
        (
            _("Additional Information"),
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """
    Admin class for Warehouse model.
    """

    list_display = [
        "id",
        "product",
        "total_balance",
        "reserved_quantity",
        "free_balance",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = [
        "product",
    ]
    search_fields = [
        "product__name",
        "product__product_code",
    ]
    search_help_text = _("Search for warehouse instances by product name and it's product code")
    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product",
                    "total_balance",
                ),
            },
        ),
        (
            _("Additional Information"),
            {
                "fields": ("is_active", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def reserve(self, obj):
        """
        Returns the quantity of the product reserved from the warehouse.
        """
        return obj.reserve

    reserve.short_description = _("Reserved Quantity")
    reserve.admin_order_field = "reserve"

    def free_balance(self, obj):
        """
        Returns the quantity of the product available for order.
        """
        return obj.free_balance

    free_balance.short_description = _("Free Balance")
    free_balance.admin_order_field = "free_balance"