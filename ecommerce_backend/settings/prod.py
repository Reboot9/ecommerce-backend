# ruff: noqa
from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

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
    "alternate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Enable throttling in DRF
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "apps.base.throttling.CustomAnonThrottle",
        "apps.base.throttling.AuthenticationRateThrottle",
        "apps.base.throttling.UserThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth": "3/minute",
        "anon": "30/hour",
        "authenticated": "15/minute",
        "admin": None,
    },
    "EXCEPTION_HANDLER": "apps.base.throttling.throttling_exception_handler",
}

# Set cache ttl to 15 minutes
CACHE_TTL = 60 * 15
