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
    entrance = serializers.CharField(required=False)
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
                    {
                        "option": "`option` field is required. "
                        "Possible choices are: `C` for courier and `D` for delivery."
                    }
                )

            # Perform additional validation based on the option value
            option = attrs.get("option")
            required_fields = []
            if option == Delivery.DeliveryOptionChoices.COURIER:
                required_fields = ["street", "entrance", "time"]
                if not (attrs.get("house") or attrs.get("flat")):
                    raise serializers.ValidationError(
                        "Either house or flat is required for courier delivery."
                    )
            elif option == Delivery.DeliveryOptionChoices.DELIVERY:
                required_fields = ["department"]

            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError({f"{field}": f"Field '{field}' is required"})

        return attrs

    def to_representation(self, instance):
        """
        Convert model instance to a dictionary for serialization.

        :param instance: Delivery instance to be serialized.
        :return: serialized representation of Delivery.
        """
        representation = super().to_representation(instance)
        option = dict(Delivery.DeliveryOptionChoices.choices).get(representation["option"])
        representation["option"] = option

        return representation

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
