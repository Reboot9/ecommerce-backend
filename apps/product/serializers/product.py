"""
Serializers related to Product model.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.product.models import Product
from apps.product.models.product import TypeProductCharacteristics
from apps.product.serializers.image import ImageSerializer
from apps.product.serializers.manufacturer import ManufacturerSerializer


class TypeProductCharacteristicsSerializer(serializers.ModelSerializer):
    """Serializer that used for TypeProductCharacteristics."""

    productCharacteristics = serializers.UUIDField(
        source="product_characteristics.name", read_only=True
    )
    typeCharacteristic = serializers.CharField(source="name", max_length=256)

    class Meta:
        model = TypeProductCharacteristics
        fields = ["productCharacteristics", "typeCharacteristic"]


class ProductListSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for list of products."""

    typesProduct = TypeProductCharacteristicsSerializer(many=True, source="types_product")
    priceDiscount = serializers.DecimalField(
        source="price_discount", max_digits=10, decimal_places=2, read_only=True
    )
    productCode = serializers.CharField(
        source="product_code",
        read_only=True,
    )
    descriptionShort = serializers.CharField(
        source="description_short",
        max_length=256,
        read_only=True,
    )
    discountPercentage = serializers.DecimalField(
        source="discount_percentage",
        max_digits=4,
        decimal_places=2,
        read_only=True,
    )
    categories = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "productCode",
            "descriptionShort",
            "price",
            "priceDiscount",
            "categories",
            "discountPercentage",
            "typesProduct",
            "image",
            "rating",
        ]
        read_only_fields = ["id", "priceDiscount"]


class ProductDetailSerializer(ProductListSerializer):
    """Serializer for detail product."""

    manufacturer = ManufacturerSerializer()
    images = ImageSerializer(many=True)

    class Meta(ProductListSerializer.Meta):
        model = Product
        fields = [
            field for field in ProductListSerializer.Meta.fields if field != "descriptionShort"
        ] + ["manufacturer", "description", "images"]
        read_only_fields = ProductListSerializer.Meta.fields


class LiteProductSerializer(serializers.ModelSerializer):
    """Simplified version of product serializer to be used in pair with other serializers."""

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "categories",
            "rating",
            "image",
            "price",
        ]
        read_only_fields = [
            "name",
            "slug",
            "categories",
            "rating",
            "image",
            "price",
        ]
