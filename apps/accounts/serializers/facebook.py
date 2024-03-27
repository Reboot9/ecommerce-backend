"""
Contains serializer for facebook auth provider
"""

from ..social_auth.register import register_social_user
from ..social_auth.facebook import Facebook

from rest_framework import serializers


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)

        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        email = user_data['email']
        provider = 'facebook'

        return register_social_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            provider=provider,
        )