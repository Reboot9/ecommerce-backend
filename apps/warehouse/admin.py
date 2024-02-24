"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.
"""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Case, Value, When
from django.utils.translation import gettext_lazy as _

from apps.warehouse.forms import WarehouseItemForm
from apps.warehouse.models import (
    WarehouseItem,
    GoodsConsumption,
    ConsignmentNote,
    GoodsArrival,
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


class WarehouseItemInline(GenericTabularInline):
    """
    Inline for managing WarehouseItem objects in the admin.
    """

    model = WarehouseItem
    extra = 1
    form = WarehouseItemForm


class ConsignmentNoteInline(admin.StackedInline):
    """
    Inline for managing ConsignmentNote objects in the admin.
    """

    model = ConsignmentNote
    fields = ("number", "sign_date")
    extra = 1
    can_delete = False


@admin.register(GoodsArrival)
class GoodsArrivalAdmin(admin.ModelAdmin):
    """
    Admin class for Goods Arrival model.
    """

    list_display = [
        "id",
        "consignment_number",
        "consignment_sign_date",
        "arrival_type",
        "comment",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "arrival_type",
        "consignmentnote__sign_date",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["consignmentnote"]
    search_fields = ["consignmentnote__number", "comment"]
    search_help_text = "Search for consignment notes by number or comment"
    date_hierarchy = "consignmentnote__sign_date"  # Consider changing this field
    inlines = [ConsignmentNoteInline, WarehouseItemInline]
    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")

    def consignment_number(self, obj) -> str:
        """
        Returns the consignment note number associated with the given object.
        """
        return obj.consignmentnote.number if obj.consignmentnote else None

    consignment_number.short_description = _("Consignment Note Number")

    def consignment_sign_date(self, obj) -> str:
        """
        Returns the consignment note sign date associated with the given object.
        """
        return obj.consignmentnote.sign_date if obj.consignmentnote else None

    consignment_sign_date.short_description = _("Consignment Note Sign Date")


@admin.register(GoodsConsumption)
class GoodsConsumptionAdmin(admin.ModelAdmin):
    """
    Admin class for Goods Consumption model.
    """

    list_display = [
        "id",
        "consignment_number",
        "consignment_sign_date",
        "consumption_type",
        "comment",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "consumption_type",
        "consignmentnote__sign_date",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["consignmentnote"]
    search_fields = ["consignmentnote__number", "comment"]
    search_help_text = "Search for consignment notes by number or comment"
    date_hierarchy = "consignmentnote__sign_date"  # Consider changing this field
    inlines = [ConsignmentNoteInline, WarehouseItemInline]
    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")

    def consignment_number(self, obj) -> str:
        """
        Returns the consignment note number associated with the given object.
        """
        return obj.consignmentnote.number if obj.consignmentnote else None

    consignment_number.short_description = _("Consignment Note Number")

    def consignment_sign_date(self, obj) -> str:
        """
        Returns the consignment note sign date associated with the given object.
        """
        return obj.consignmentnote.sign_date if obj.consignmentnote else None

    consignment_sign_date.short_description = _("Consignment Note Sign Date")


@admin.register(ConsignmentNote)
class ConsignmentNoteAdmin(admin.ModelAdmin):
    """
    Admin class for Consignment Note model.
    """

    list_display = [
        "id",
        "number",
        "sign_date",
        "is_goods_arrival",
        "is_goods_consumption",
        "created_at",
        "updated_at",
    ]
    list_filter = ["sign_date", "created_at", "updated_at"]
    search_fields = ["number"]
    date_hierarchy = "sign_date"
    search_help_text = _("Search for consignment notes by number")
    readonly_fields = ("created_at", "updated_at")

    def is_goods_arrival(self, obj) -> bool:
        """
        Determines whether the given object has a related goods arrival.
        """
        return obj.goods_arrival is not None

    is_goods_arrival.boolean = True
    is_goods_arrival.short_description = "Is Arrival"

    def is_goods_consumption(self, obj) -> bool:
        """
        Determines whether the given object has a related goods consumption.
        """
        return obj.goods_consumption is not None

    is_goods_consumption.boolean = True
    is_goods_consumption.short_description = "Is Consumption"


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    """
    Admin class for Reserve model.
    """

    actions = [toggle_is_active]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """
    Admin class for Warehouse model.
    """

    readonly_fields = ("created_at", "updated_at")
