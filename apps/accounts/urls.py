"""
Accounts app URLs.

This module defines the URL patterns for the accounts app. The accounts app is responsible for
handling user authentication, registration, and profile-related views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.views.facebook import FacebookSocialAuthView
from apps.accounts.views.google import GoogleSocialAuthView
from apps.accounts.views.user import UserViewSet

app_name = "accounts"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/google/", GoogleSocialAuthView.as_view()),
    path("auth/facebook/", FacebookSocialAuthView.as_view()),
]
