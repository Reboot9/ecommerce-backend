"""
Django Admin configurations.

This module provides the configuration for the Django admin interface.
"""
import json

from django.contrib import admin

from django.contrib import messages
from django.db.models import Case, Value, When
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from apps.warehouse.forms import WarehouseTransactionForm
from apps.warehouse.models import (
    ConsignmentNote,
    Transaction,
    Reserve,
    Warehouse,
)

from apps.warehouse.serializers.warehouse import WarehouseSerializer


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


@admin.action(description="Generate report for chosen items at the Warehouse")
def generate_transactions_report(modeladmin, request, queryset):
    """
    Action to generate transactions report based on dates of transactions and exported filetype.
    """
    selected_warehouses = queryset.values_list("pk", flat=True)
    if "apply" in request.POST:
        form = WarehouseTransactionForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            file_type = form.cleaned_data["file_type"]

            # Available renderers for model
            file_type_renderers = {
                "json": JSONRenderer(),
                "xml": XMLRenderer(),
            }

            if file_type not in file_type_renderers:
                messages.error(request, "Unsupported file type")
                return render(
                    request,
                    "admin/warehouse_transaction_report.html",
                    {"items": queryset, "form": form},
                )
            # Serialize warehouse and transactions data
            warehouse_serializer = WarehouseSerializer(
                queryset, many=True, context={"start_date": start_date, "end_date": end_date}
            )
            renderer = file_type_renderers[file_type]
            report_data = renderer.render(warehouse_serializer.data)

            # Prettify JSON output with an indent of 4 spaces
            if file_type == "json":
                report_data = json.dumps(json.loads(report_data), indent=4)

            response = HttpResponse(report_data, content_type=f"text/{file_type}")
            formatted_start_date = start_date.strftime("%d.%m.%Y")
            formatted_end_date = end_date.strftime("%d.%m.%Y")
            file_name = (
                f"warehouse_transactions_report_"
                f"{formatted_start_date}-{formatted_end_date}.{file_type}"
            )
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'

            return response
        else:
            # Display form errors
            messages.error(request, form.errors)
            return render(
                request,
                "admin/warehouse_transaction_report.html",
                {"items": queryset, "form": form},
            )

    form = WarehouseTransactionForm(initial={"_selected_action": selected_warehouses})

    return render(
        request, "admin/warehouse_transaction_report.html", {"items": queryset, "form": form}
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
        "product_category",
        "total_balance",
        "reserved_quantity",
        "free_balance",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "product__categories__name",
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
        "product__categories__name",
    ]
    search_help_text = _("Search for warehouse instances by product name and it's product code")
    actions = [toggle_is_active, generate_transactions_report]
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

    def product_category(self, obj):
        """
        Returns the product category.
        """
        return obj.product.categories

    product_category.short_description = _("Product Category")
