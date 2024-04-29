"""
This module defines the serializers for Delivery model.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.delivery import Delivery


class DeliverySerializer(BaseDateSerializer, serializers.ModelSerializer):
    """
    Serializer for Delivery model.

    This serializer handles the serialization and deserialization of Delivery objects.
    """

    street = serializers.CharField(required=False)
    house = serializers.CharField(required=False)
    flat = serializers.CharField(required=False)
    floor = serializers.IntegerField(required=False)
    entrance = serializers.IntegerField(required=False)
    department = serializers.CharField(required=False)
    time = serializers.DateField(required=False)
    declaration = serializers.CharField(required=False)
    option = serializers.ChoiceField(
        required=False,
        choices=Delivery.DeliveryOptionChoices,
    )

    class Meta:
        model = Delivery
        exclude = ("created_at", "updated_at")

        read_only_fields = ("id",)

    def validate(self, attrs):
        """
        Validate method to ensure option field is required when creating an instance.
        """
        if self.instance is None:
            # If creating an instance, option field is required
            if "option" not in attrs:
                raise serializers.ValidationError(
                    "`option` field is required. "
                    "Possible choices are: `C` for courier and `D` for delivery."
                )
        return attrs

    # TODO: Consider about enabling this method to remove unused fields based on delivery option.
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     if instance.option == Delivery.DeliveryOptionChoices.COURIER:
    #         ret["street"] = instance.street
    #         ret["house"] = instance.house
    #         ret["entrance"] = instance.entrance
    #         ret["time"] = instance.time
    #         # Remove department related fields
    #         ret.pop("department", None)
    #     else:
    #         ret["department"] = instance.department
    #         # Remove courier related fields
    #         ret.pop("street", None)
    #         ret.pop("house", None)
    #         ret.pop("entrance", None)
    #         ret.pop("time", None)
    #
    #     return ret
