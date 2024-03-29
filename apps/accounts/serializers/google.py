"""
Contains serializer for google auth provider.
"""
from rest_framework import serializers

from apps.accounts.social_auth.register import register_social_auth
from apps.accounts.social_auth.google import GoogleAuthAPI

from typing import Dict, Any


class GoogleSocialAuthSerializer(serializers.Serializer):
    """
    Google serilizaer which validate auth token.
    """

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token: str):
        """
        Validate token provide by frontend part of application.

        :param auth_token: token from frontend part
        :return: Dict[user_data, tokens[Access, Refresh]]
        """
        user_data: Dict[str, Any] = GoogleAuthAPI.validate(auth_token)

        if not isinstance(user_data, dict):
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again!"
            )

        # if user_data.get("aud") != os.environ.get("GOOGLE_CLIENT_ID", ""):
        #     raise AuthenticationFailed(
        #         "Try to authorize from unknown google client."
        #     )

        first_name = user_data.get("given_name")
        last_name = user_data.get("family_name")
        email = user_data.get("email")
        provider = "google"

        return register_social_auth(
            email=email, first_name=first_name, last_name=last_name, provider=provider
        )
