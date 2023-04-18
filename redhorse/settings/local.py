from .base import *

DEBUG = True

SECRET_KEY = env("SECRET_KEY")


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Django REST Framework

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%b %d, %Y",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}


# CORS

CORS_ALLOWED_ORIGINS = [
    f"http://{env('LOCAL_FRONTEND_DOMAIN')}",
]
