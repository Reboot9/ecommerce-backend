"""
Contains serializer for facebook auth provider.
"""

from apps.accounts.social_auth.register import register_social_auth
from apps.accounts.social_auth.facebook import FacebookAuthAPI

from rest_framework import serializers


class FacebookSocialAuthSerializer(serializers.Serializer):
    """
    Handles serialization of facebook related data.
    """

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token: str):
        """
        Validate token given by frontend part of application.
        """
        user_data: dict = FacebookAuthAPI.validate(auth_token)

        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        provider = "facebook"

        return register_social_auth(
            email=email, first_name=first_name, last_name=last_name, provider=provider
        )
