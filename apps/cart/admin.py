"""
Module: admin.py.

This module contains the admin configurations for the cart app.
"""

from django.contrib import admin

from apps.cart.models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    """Inline admin class for CartItem related to Cart."""

    model = CartItem
    extra = 2
    verbose_name = "Cart item"
    verbose_name_plural = "Cart items"


class CartAdmin(admin.ModelAdmin):
    """Admin class for Cart model."""

    inlines = [CartItemInline]
    list_display = (
        "id",
        "user",
        "total_quantity",
        "total_price",
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("user",)
    search_help_text = "In this field you can search by such fields: user"
    list_filter = ("is_active", "created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


class CartItemAdmin(admin.ModelAdmin):
    """Admin class for CartItem model."""

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "price",
        "discount_percentage",
        "cost",
    )
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("cart",)
    autocomplete_fields = ("product",)
    search_fields = ("product", "cart")
    search_help_text = "In this field you can search by such fields: product, cart"
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
