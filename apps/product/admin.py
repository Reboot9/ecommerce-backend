"""
Module: admin.py.

This module contains the admin configurations for the product app.
"""

from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from apps.product.models import Manufacturer, Category, Image
from apps.product.models.product import ProductCharacteristics, TypeProductCharacteristics, Product


class TypeProductCharacteristicsInline(admin.TabularInline):
    """Inline class for TypeProductCharacteristics related to Product."""

    model = TypeProductCharacteristics.product.through
    extra = 1
    verbose_name = "Type of product characteristic"
    verbose_name_plural = "Type of product characteristics"


class ProductCharacteristicsInline(admin.TabularInline):
    """Inline admin class for ProductCharacteristics related to Product."""

    model = ProductCharacteristics.product.through
    extra = 1
    verbose_name = "Product Characteristic"
    verbose_name_plural = "Product Characteristics"


class ImageInline(admin.TabularInline):
    """Inline admin class for Image related to Product."""

    model = Image
    extra = 2
    verbose_name = "Additional image"
    verbose_name_plural = "Additional images"


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
        "updated_at",
    )
    list_select_related = ("manufacturer", "categories")
    readonly_fields = ("created_at", "updated_at")
    search_fields = (
        "name",
        "product_code",
        "slug",
        "manufacturer__trade_brand",
        "categories__name",
    )
    search_help_text = (
        "In this field you can search by such fields: name,"
        " product code, slug, manufacturer, categories"
    )
    autocomplete_fields = ("manufacturer", "categories")
    list_filter = ("stock", "discount_percentage", "created_at", "updated_at")
    list_editable = ("price", "discount_percentage", "stock")
    prepopulated_fields = {"slug": ("name", "product_code")}
    actions = ("remove_discount",)
    inlines = (
        ProductCharacteristicsInline,
        TypeProductCharacteristicsInline,
        ImageInline,
    )  # inline will change
    list_per_page = 10
    list_max_show_all = 100


class ProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for ProductCharacteristics model."""

    list_display = ("product_characteristic", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("product_characteristic",)
    search_help_text = "In this field you can search by such fields: product characteristic"
    list_filter = ("created_at", "updated_at")
    filter_horizontal = ("product", "categories")
    list_per_page = 10
    list_max_show_all = 100


class TypeProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for TypeProductCharacteristics model."""

    list_display = ("type_characteristic", "product_characteristics", "created_at", "updated_at")
    list_select_related = ("product_characteristics",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("type_characteristic",)
    search_help_text = "In this field you can search by such fields: type characteristic"
    list_filter = ("created_at", "updated_at")
    filter_horizontal = ("product",)
    list_per_page = 10
    list_max_show_all = 100
    autocomplete_fields = ("product_characteristics",)


class ManufacturerAdmin(admin.ModelAdmin):
    """Admin class for Manufacturer mode."""

    list_display = (
        "trade_brand",
        "country",
        "country_brand_registration",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("trade_brand", "country")
    search_help_text = "In this field you can search by such fields: trade brand, country"
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


class CategoryAdmin(admin.ModelAdmin):
    """Admin class for Category model."""

    list_display = ("__str__", "slug", "parent_link", "level", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_filter = ("level",)
    ordering = ("level", "created_at")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("parent",)

    def parent_link(self, obj):
        """Method to generate link to parent, if exists."""
        if obj.parent:
            url = reverse("admin:product_category_change", args=[obj.parent.id])
            return format_html('<a href="{}">{}</a>', url, obj.parent.name)
        return "-"

    parent_link.short_description = "Parent Category"

    def get_form(self, request, obj=None, **kwargs):
        """
        Customizes the form used in the CategoryAdmin.

        To exclude the currently edited category from the 'parent' field options.

        :param request: The HTTP request object.
        :param obj: The current Category instance being edited or None for a new instance.
        :param kwargs: Additional keyword arguments passed to the method.
        :return: The customized form.
        """
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)  # noqa: UP008

        # Remove obj that is edited from relevant options
        form.base_fields["parent"].queryset = Category.objects.exclude(
            pk=obj.pk if obj else None,
        )

        # TODO: exclude categories as parent option that are greater than selected category level \
        #  every time user clicks on level (more likely via js)
        # .exclude(level__gte=obj.level if obj else 0)

        return form


class ImageAdmin(admin.ModelAdmin):
    """Admin class for Image model."""

    list_display = ("image", "product", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("product__name",)
    search_help_text = "In this field you can search by such fields: product name"
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100
    autocomplete_fields = ("product",)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCharacteristics, ProductCharacteristicsAdmin)
admin.site.register(TypeProductCharacteristics, TypeProductCharacteristicsAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
