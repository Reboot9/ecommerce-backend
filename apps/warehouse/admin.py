"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.
"""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.warehouse.forms import WarehouseItemForm
from apps.warehouse.models import (
    WarehouseItem,
    GoodsConsumption,
    ConsignmentNote,
    GoodsArrival,
    Reserve,
    Warehouse,
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

    inlines = [WarehouseItemInline, ConsignmentNoteInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(GoodsConsumption)
class GoodsConsumptionAdmin(admin.ModelAdmin):
    """
    Admin class for Goods Consumption model.
    """

    inlines = [WarehouseItemInline, ConsignmentNoteInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(ConsignmentNote)
class ConsignmentNoteAdmin(admin.ModelAdmin):
    """
    Admin class for Consignment Note model.
    """

    readonly_fields = ("created_at", "updated_at")


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    """
    Admin class for Reserve model.
    """

    readonly_fields = ("created_at", "updated_at")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """
    Admin class for Warehouse model.
    """

    readonly_fields = ("created_at", "updated_at")
