"""
Module: admin.py.

This module contains the admin configurations for the product app.
"""

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from apps.product.models import Manufacturer, Category, Image
from apps.product.models.product import ProductCharacteristics, TypeProductCharacteristics, Product


class TypeProductCharacteristicsInline(admin.TabularInline):
    """Inline class for TypeProductCharacteristics related to Product."""

    model = TypeProductCharacteristics.product.through
    extra = 1


class ProductCharacteristicsInline(admin.TabularInline):
    """Inline admin class for ProductCharacteristics related to Product."""

    model = ProductCharacteristics.product.through
    extra = 1


class ImageInline(admin.TabularInline):
    """Inline admin class for Image related to Product."""

    model = Image
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    """Admin class for Product model."""

    @admin.action(description="Remove promotional discount")
    def remove_discount(self, request, queryset):
        """Custom admin action to remove promotional discount."""
        updated = queryset.update(discount_percentage=0)
        self.message_user(
            request,
            ngettext(
                "%d discount successfully removed.", "%d discounts successfully removed.", updated
            )
            % updated,
            messages.SUCCESS,
        )

    list_display = (
        "slug",
        "name",
        "price",
        "stock",
        "manufacturer",
        "categories",
        "discount_percentage",
        "price_discount",
        "created_at",
    )
    search_fields = ("name", "product_code")
    list_filter = ("stock", "discount_percentage")
    list_editable = ("price", "discount_percentage", "stock")
    prepopulated_fields = {"slug": ("name", "product_code")}
    actions = ("remove_discount",)
    inlines = (TypeProductCharacteristicsInline, ProductCharacteristicsInline)


class ProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for ProductCharacteristics model."""

    List_display = ("product_charactetistic", "categories")
    filter_horizontal = ("product",)


class TypeProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for TypeProductCharacteristics model."""

    list_display = ("type_characteristic",)
    search_fields = ("type_characteristic",)
    filter_horizontal = ("product",)


class ManufacturerAdmin(admin.ModelAdmin):
    """Admin class for Manufacturer mode."""

    list_display = ("trade_brand",)


class CategoryAdmin(admin.ModelAdmin):
    """Admin class for Category model."""

    list_display = (
        "id",
        "name",
    )


class ImageAdmin(admin.ModelAdmin):
    """Admin class for Image model."""

    list_display = ("image",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCharacteristics, ProductCharacteristicsAdmin)
admin.site.register(TypeProductCharacteristics, TypeProductCharacteristicsAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
