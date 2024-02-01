"""
Module: admin.py.

This module contains the admin configurations for the order app.
"""

from django.contrib import admin

from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin class for OrderItem related to Order."""

    model = OrderItem
    extra = 2
    autocomplete_fields = ("product",)
    verbose_name = "Order item"
    verbose_name_plural = "Order Items"


class OrderAdmin(admin.ModelAdmin):
    """Admin class for Order model."""

    list_display = (
        "order_number",
        "first_name",
        "last_name",
        "status",
        "phone",
        "email",
        "comment",
        "is_paid",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("first_name", "last_name", "phone", "email")
    list_filter = ("status", "is_paid", "created_at", "updated_at")
    list_editable = ("status", "is_paid")
    inlines = (OrderItemInline,)
    list_per_page = 10
    list_max_show_all = 100


class OrderItemAdmin(admin.ModelAdmin):
    """Admin class for OrderItem model."""

    list_display = ("order", "price", "product", "quantity", "created_at", "updated_at")
    list_select_related = ("order",)
    autocomplete_fields = ("product",)  # only ForeignKey or ManyToMany
    list_filter = ("created_at", "updated_at")
    search_fields = ("product", "order")
    list_per_page = 10
    list_max_show_all = 100


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
