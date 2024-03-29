"""
Module contains facebook oAUTH view.
"""
from rest_framework import generics, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.accounts.serializers.facebook import FacebookSocialAuthSerializer
from apps.accounts import schemas


class FacebookSocialAuthView(generics.GenericAPIView):
    """
    View register or autheficate user in system by facebook provider.
    """

    serializer_class = FacebookSocialAuthSerializer

    @swagger_auto_schema(
        operation_description="Login with Facebook",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_token": schemas.social_auth_token,
            },
            required=["auth_token"],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User authficated by Facebook GraphAPI successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": schemas.user_response_schema,
                        "tokens": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "access": schemas.access_token_schema,
                                "refresh": schemas.refresh_token_schema,
                            },
                        ),
                    },
                ),
            )
        },
    )
    def post(self, request):
        """
        POST with "auth_token".

        Send an access token as from facebook to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
