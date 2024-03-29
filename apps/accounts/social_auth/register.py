"""
Module have creation user method for social auth providers.
"""
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers.user import UserSerializer
from django.contrib.auth import authenticate
from apps.accounts.models import CustomUser

import os


def get_user_with_tokens(instance: CustomUser) -> list:
    """
    Get user instance model and return JSON user data with tokens.

    :return: List[user_data, access_token, refresh_token]
    """
    tokens = RefreshToken.for_user(instance)
    data = UserSerializer(instance=instance).data

    return data, str(tokens.access_token), str(tokens)


def register_social_auth(
    *,
    email: str,
    first_name: str,
    last_name: str,
    provider: str,
):
    """
    Register user in system by social_auth provider, such as google or facebook oAUTH API.

    :param email: given by provider
    :param first_name: given by provider
    :param last_name: given by provider
    :param provider: given by serializer provider
    :return: Dict[user_data, tokens[Access, Refresh]]
    """
    try_find_user = CustomUser.objects.filter(email=email)
    users_password = os.environ.get("SOCIAL_USERS_SECRET")

    if try_find_user.exists():
        auth_provider = try_find_user[0].auth_provider

        if provider == auth_provider:
            registered_user = authenticate(
                email=email,
                password=users_password,
            )

            user_data, access, refresh = get_user_with_tokens(registered_user)

            return {
                "user": user_data,
                "tokens": {"access": access, "refresh": refresh},
            }
        else:
            raise AuthenticationFailed("Please continue your login by using " + auth_provider)

    else:
        user = CustomUser.objects.create_user(
            email=email,
            password=users_password,
            first_name=first_name,
            last_name=last_name,
            auth_provider=provider,
        )
        user.save()

        new_user = authenticate(
            email=email,
            password=users_password,
        )

        user_data, access, refresh = get_user_with_tokens(new_user)

        return {
            "user": user_data,
            "tokens": {"access": access, "refresh": refresh},
        }
