"""
This module contains Django views related to user authentication and creation.
"""
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import QuerySet
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
from apps.base.mixins import CachedListView
from apps.base.pagination import PaginationCommon

# TODO: consider about adding more Swagger things like tags
#  and implement authentication in Swagger via JWT

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


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


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="List all users with pagination",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Page number",
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of items per page",
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of users",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "next": openapi.Schema(type=openapi.TYPE_STRING),
                        "previous": openapi.Schema(type=openapi.TYPE_STRING),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=schemas.user_response_schema,
                        ),
                    },
                ),
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
class UserViewSet(CachedListView, viewsets.ModelViewSet):
    """
    User management API.
    """

    serializer_class = UserSerializer
    pagination_class = PaginationCommon

    def get_queryset(self) -> QuerySet[CustomUser]:
        """
        Retrieve the queryset for CustomUser instances.

        :return: The queryset for CustomUser instances.
        """
        # Only include active users in the queryset
        return CustomUser.objects.filter(is_active=True)

    def get_cache_key(self, user_id=None) -> str:
        """
        Method to get cache key.

        :param user_id: unique identifier of user
        :return: cache key for the provided user
        """
        if user_id is not None:
            return f"user_detail_{self.request.path}?{self.request.GET.urlencode()}"

        return f"user_list:{self.request.path}?{self.request.GET.urlencode()}"

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a single user by their id.

        :param request: The HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: details of the requested user.
        """
        user_id = kwargs["pk"]
        cache_key = self.get_cache_key(user_id)

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)

    def perform_create(self, serializer) -> None:
        """
        Perform actions when creating instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        # Clear the list cache when a new user is created
        instance = serializer.save()
        # Clear the list cache when a new order is created
        cache.delete("user_list")
        return instance

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
                                "access": schemas.access_token_schema,
                                "refresh": schemas.refresh_token_schema,
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

        :param request: The HTTP request containing user data.
        :param args: Variable-length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: Response object indicating the operation status. If successful, returns a
        response with the newly created user data and associated access and refresh tokens.
        If unsuccessful, returns a response with error details.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Add access and refresh tokens to response properties
            refresh = RefreshToken.for_user(user)
            tokens = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }

            return Response(
                {"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer) -> None:
        """
        Perform actions when updating CustomUser instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        instance = serializer.save()
        # Clear individual user cache and list cache
        user_id = self.kwargs.get("pk")
        cache.delete(self.get_cache_key(user_id))
        cache.delete("user_list")

        return instance

    def perform_destroy(self, instance) -> None:
        """
        Perform actions when deleting CustomUser instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        # Clear individual user cache and list cache
        user_id = self.kwargs.get("pk")
        cache.delete(instance.get_cache_key(user_id))
        cache.delete("user_list")

    @swagger_auto_schema(
        operation_description="Delete user",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="User deleted successfully"),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="User not found", schema=schemas.detail_schema
            ),
        },
    )
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete of user instance by setting is_active to False.

        :param request: The HTTP request object.
        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: Response object with a status of 204 (No content)
         indicating successful deletion
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
