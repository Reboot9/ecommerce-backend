"""
Contains serializers for tokens, required to generate swagger in drf-yasg library.
"""
from typing import Any

from rest_framework import serializers


class TokenObtainPairResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of obtaining a JSON Web Token pair.

    Attributes:
        - access (str): The access token obtained.
        - refresh (str): The refresh token obtained.

    """

    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data: dict) -> Any:
        """
        Not implemented. This method is required by the parent class `Serializer`.
        """
        raise NotImplementedError()

    def update(self, instance: Any, validated_data: dict) -> Any:
        """
        Not implemented. This method is required by the parent class `Serializer`.
        """
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    """
    Serializer for the response of refreshing a JSON Web Token.

    Attributes:
        - access (str): The new access token obtained.
    """

    access = serializers.CharField()

    def create(self, validated_data: dict) -> Any:
        """
        Not implemented. This method is required by the parent class `Serializer`.
        """
        raise NotImplementedError()

    def update(self, instance: Any, validated_data: dict) -> Any:
        """
        Not implemented. This method is required by the parent class `Serializer`.
        """
        raise NotImplementedError()
