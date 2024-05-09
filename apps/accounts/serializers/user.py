"""
Contains serializers for user-related models and registration logic.
"""
from typing import Dict, Any

from rest_framework import serializers

from apps.accounts.models import CustomUser
from apps.accounts.utils import validate_password_format


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, handling user registration.
    """

    password = serializers.CharField(
        max_length=128, min_length=8, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=128, min_length=8, style={"input_type": "password"}, write_only=True
    )
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "password2",
            "createdAt",
            "updatedAt",
        )

    def get_fields(self) -> Dict[str, Any]:
        """
        Override the get_fields method to customize field behavior based on the HTTP method.

        During update operations (PATCH or PUT), exclude the email and password fields from the
        serialized output and do not expect them in the incoming data.

        :return: A dictionary of field names and their corresponding serializer instances.

        """
        fields = super().get_fields()
        request_method = self.context["request"].method if "request" in self.context else None

        # Remove email and password fields during update operation
        if request_method == "PATCH" or request_method == "PUT":
            fields.pop("email", None)
            fields.pop("password", None)
            fields.pop("password2", None)

        return fields

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

        # Validate the password format
        password = data.get("password")
        if password:
            if not validate_password_format(password):
                raise serializers.ValidationError(
                    {
                        "password": "Password must contain only latin letters, numbers, and"
                        " special characters (!\"#$%&'()*+,-./:;<>?=@[\\]^_`{|}~).",
                        "password2": "Password must contain only latin letters, numbers, and"
                        " special characters (!\"#$%&'()*+,-./:;<>?=@[\\]^_`{|}~).",
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
