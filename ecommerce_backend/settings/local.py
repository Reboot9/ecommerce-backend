# noqa
from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

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
