"""
Contains serializers for user-related models and registration logic.
"""
from typing import Dict, Any

from rest_framework import serializers

from apps.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, handling user registration.
    """

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "password2",
        )

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the passwords match during registration.
        """
        if (
            data.get("password")
            and data.get("password2")
            and data["password"] != data["password2"]
        ):
            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match.",
                    "password2": "Passwords do not match.",
                }
            )
        return data

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """
        Create a new user instance during registration.
        """
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance: CustomUser, validated_data: Dict[str, Any]) -> CustomUser:
        """
        Update an existing model instance.

        :param instance: The existing user instance to be updated.
        :param validated_data: The validated data containing the fields to be updated.
        :return: The updated user instance.
        """
        # Prevent modifying the email field after creation
        if "email" in validated_data:
            raise serializers.ValidationError("Email cannot be modified after creation.")

        # Call the default update method for other fields
        return super().update(instance, validated_data)
