"""
Contains serializer for google auth provider
"""

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers

from ..social_auth.register import register_social_user
from ..social_auth.google import Google

from typing import Dict, Any
import os


class GoogleSocialAuthSerializer(
    serializers.Serializer
):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token: str):
        """
        Validate token provide by google success auth

        :param auth_token: token from google api
        :return: Dict[user_data, tokens[acces, refresh]]
        """

        user_data: Dict[str, Any] = Google.validate(auth_token)

        if not isinstance(user_data, dict):
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again!"
            )
        
        if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed(
                "Try to authorize from unknown google client."
            )

        first_name = user_data["given_name"]
        last_name = user_data["family_name"]
        email = user_data["email"]
        provider = "google"

        return register_social_user(
            first_name=first_name,
            last_name=last_name,
            provider=provider,
            email=email, 
        )


