# ruff: noqa
from .base import *  # noqa: F403
import socket

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE.insert(
        0,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


def get_internal_ips() -> list[str]:
    """
    Get internal IPs required for Django Debug Toolbar in a Docker environment.

    Returns:
        list: List of internal IP addresses.
    """
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    internal_ips = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

    # Since our requests will be routed to Django via the nginx container, include
    # the nginx IP address as internal as well
    try:
        nginx_hostname, _, nginx_ips = socket.gethostbyname_ex("nginx")
        internal_ips += nginx_ips
    except socket.gaierror:
        # since nginx may not be started at the point that this is first executed.
        pass
    return internal_ips


INTERNAL_IPS = get_internal_ips()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),  # This should be container name
        "PORT": os.environ.get("DB_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # REDIS_HOST has to be container name
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    # "alternate": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     },
    # },
}

# REST_FRAMEWORK = {
#     "DEFAULT_THROTTLE_CLASSES": [
#         "apps.base.throttling.CustomAnonThrottle",
#         "apps.base.throttling.AuthenticationRateThrottle",
#         "apps.base.throttling.UserThrottle",
#     ],
#     "DEFAULT_THROTTLE_RATES": {
#         "auth": "3/minute",
#         "anon": "30/hour",
#         "authenticated": "15/minute",
#         "admin": None,
#     },
#     "EXCEPTION_HANDLER": "apps.base.throttling.throttling_exception_handler",
# }

# Set cache ttl to 15 minutes
CACHE_TTL = 60 * 15
