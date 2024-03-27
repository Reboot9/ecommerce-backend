from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.user import UserSerializer
from django.contrib.auth import authenticate
from ..models import CustomUser

import os


def register_social_user(
    email: str,
    first_name: str,
    last_name: str,
    *,
    provider: str

):
    
    """
    Register user in system by google ot facebook oAUTH API

    :param email: user email
    :param first_name: user first name
    :param last_name: user last name
    :param provider: oAUTH API provider

    :return: Dict[user_data, tokens[acces, refresh]]

    """

    try_find_user = CustomUser.objects.filter(email=email)
    user_password = os.environ.get("SOCAIL_USERS_SECRET")
    
    if try_find_user.exists():
        auth_provider = try_find_user[0].auth_provider 
        
        if provider == auth_provider:

            registered_user = authenticate(
                password=user_password,
                email=email, 
            )

            refresh = RefreshToken.for_user(registered_user)
            data = UserSerializer(instance=registered_user).data
            
            return {"user": data, 
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }
                }

        else:
            raise AuthenticationFailed(
                "Please continue your login by using " + auth_provider
            )
    
    else:

        user = CustomUser.objects.create_user(
            email=email,
            password=user_password,
            first_name=first_name,
            last_name=last_name,
            auth_provider=provider
        )

        user.save()

        new_user = authenticate(
            email=email,
            pasword=user_password
        )

        refresh = RefreshToken.for_user(new_user)
        data = UserSerializer(instance=new_user).data
    
        return {"user": data, 
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            }