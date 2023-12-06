from django.shortcuts import render  # noqa F401
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import schemas
from apps.accounts.models import CustomUser
from apps.accounts.serializers.token import TokenRefreshResponseSerializer
from apps.accounts.serializers.user import UserSerializer


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


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="List all users",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of users",
                schema=openapi.Schema(type=openapi.TYPE_ARRAY, items=schemas.user_response_schema),
            ),
        },
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Retrieve user details",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User details retrieved successfully",
                schema=schemas.user_response_schema,
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found", schema=schemas.detail_schema
            ),
        },
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Update user details",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User updated successfully",
                schema=schemas.user_response_schema,
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found", schema=schemas.detail_schema
            ),
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Partially update user details",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="User partially updated successfully",
                schema=schemas.user_response_schema,
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found", schema=schemas.detail_schema
            ),
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Delete user",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="User deleted successfully"),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found", schema=schemas.detail_schema
            ),
        },
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    User management API.
    """

    # TODO: add pagination
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Registration of new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": schemas.email_schema,
                "password": schemas.password_schema,
                "password2": schemas.password_schema,
            },
            required=[
                "email",
                "password",
                "password2",
            ],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "user": schemas.user_response_schema,
                        "tokens": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "refresh": schemas.refresh_token_schema,
                                "access": schemas.access_token_schema,
                            },
                        ),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request", schema=openapi.Schema(type=openapi.TYPE_OBJECT)
            ),
        },
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create a new user based on the provided request data.

        Args:
            request (Request): The HTTP request containing user data.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Add access and refresh tokens to response properties
            refresh = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(
                {"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
