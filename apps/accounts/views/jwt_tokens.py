"""
This module contains Django views related to jwt tokens views.
"""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

from apps.accounts import schemas
from apps.accounts.serializers.token import TokenRefreshResponseSerializer

# TODO: consider about adding more Swagger things like tags
#  and implement authentication in Swagger via JWT


class DecoratedTokenObtainPairView(jwt_views.TokenObtainPairView):
    """
    Extended view for obtaining JSON Web Tokens with Swagger documentation.
    """

    @swagger_auto_schema(
        operation_description="Takes a set of user credentials and returns an access and refresh"
        " JSON web token pair to prove the authentication"
        " of those credentials.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"email": schemas.email_schema, "password": schemas.password_schema},
            required=["email", "password"],
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="JWT tokens obtained successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access": schemas.access_token_schema,
                        "refresh": schemas.refresh_token_schema,
                    },
                    required=["access", "refresh"],
                ),
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Invalid credentials", schema=schemas.detail_schema
            ),
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handles HTTP POST request to obtain JSON Web Tokens.

        :param request: The HTTP request object.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: HTTP response containing JSON Web Tokens
        """
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(jwt_views.TokenRefreshView):
    """
    Extended view for refreshing JSON Web Tokens with Swagger documentation.
    """

    @swagger_auto_schema(
        operation_description="Takes a refresh type JSON web token and returns an access type JSON"
        " web token if the refresh token is valid.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access": schemas.access_token_schema,
                "refresh": schemas.refresh_token_schema,
            },
            required=["refresh"],
        ),
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Invalid refresh token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            title="Response details.", type=openapi.TYPE_STRING
                        ),
                        "code": openapi.Schema(
                            title="Code detail error", type=openapi.TYPE_STRING
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handles HTTP POST request to refresh JSON Web Tokens.

        :param request: The HTTP request object.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: HTTP response containing JSON Web Tokens
        """
        return super().post(request, *args, **kwargs)
