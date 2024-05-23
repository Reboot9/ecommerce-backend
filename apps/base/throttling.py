"""
Settings related to throttling.
"""
import sys

from django.conf import settings
from django.core.cache import caches
from rest_framework.throttling import SimpleRateThrottle, ScopedRateThrottle, AnonRateThrottle
from rest_framework.views import exception_handler

# Check if "alternate" cache backend exists in settings
if "alternate" in caches:
    CACHE = caches["alternate"]
else:
    # If "alternate" cache backend is not defined, fallback to "default"
    CACHE = caches["default"]


def throttling_exception_handler(exc, context):
    """Custom exception handler for throttling."""
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 429:
        throttle_classes = getattr(context["view"], "throttle_classes", [])
        applied_throttle = None

        for throttle_class in throttle_classes:
            throttle_instance = throttle_class()

            # if throttle doesn't allow request, means that this instance raised ThrottleException
            if not throttle_instance.allow_request(context["request"], context["view"]):
                applied_throttle = throttle_instance.__class__.__name__
                break

        response.data = {
            "message": "Request limit exceeded. Please try again later.",
            # display time when request will be available
            "availableIn": f"{response.get('Retry-After', 'unknown')} seconds.",
            # display class that raised ThrottleException
            "throttle": applied_throttle if applied_throttle else "UnknownThrottle",
        }
    return response


class UserThrottle(SimpleRateThrottle):
    """
    Custom throttle class that applies different rates based on user type.

    This class provides throttling rules for anonymous, authenticated, and admin users.
    """

    cache = CACHE
    scope = "anon"

    def get_cache_key(self, request, view):
        """
        Generate a unique cache key based on the user's authentication status.
        """
        user = request.user
        if not user.is_authenticated:
            self.scope = "anon"
            ident = self.get_ident(request)
        else:
            if user.is_superuser or user.is_staff:
                self.scope = "admin"
            else:
                self.scope = "authenticated"

            ident = user.pk

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }

    def allow_request(self, request, view):
        """Check if request should be allowed based on throttling conditions."""
        # Allow request if tests are running
        if "test" in sys.argv:
            return True

        # Check if throttling classes are defined in settings
        if getattr(settings, "REST_FRAMEWORK", {}).get("DEFAULT_THROTTLE_CLASSES"):
            return super().allow_request(request, view)

        return True


class AuthenticationRateThrottle(ScopedRateThrottle):
    """Throttle class for authentication related views."""

    scope = "auth"
    rate = ("3/minute",)
    cache = CACHE

    def allow_request(self, request, view):
        """Check if request should be allowed based on throttling conditions."""
        # Allow request if tests are running
        if "test" in sys.argv:
            return True

        # Check if throttling classes are defined in settings
        if getattr(settings, "REST_FRAMEWORK", {}).get("DEFAULT_THROTTLE_CLASSES"):
            return super().allow_request(request, view)

        return True


class CustomAnonThrottle(AnonRateThrottle):
    """Custom AnonRateThrottle class."""

    def allow_request(self, request, view):
        """Check if request should be allowed based on throttling conditions."""
        # Check if tests are running
        if "test" in sys.argv:
            return True

        # Check if throttling classes are defined in settings
        if getattr(settings, "REST_FRAMEWORK", {}).get("DEFAULT_THROTTLE_CLASSES"):
            return super().allow_request(request, view)

        return True
