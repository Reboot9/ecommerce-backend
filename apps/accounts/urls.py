"""
Accounts app URLs.

This module defines the URL patterns for the accounts app. The accounts app is responsible for
handling user authentication, registration, and profile-related views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts import views

app_name = "accounts"

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
