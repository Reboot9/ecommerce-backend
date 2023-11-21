from django.shortcuts import render  # noqa F401
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import CustomUser
from apps.accounts.serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User management API.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs) -> Response:
        """
        Create a new user based on the provided request data.

        Args:
            request (Request): The HTTP request containing user data.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        serializer = UserSerializer(data=request.data)
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
