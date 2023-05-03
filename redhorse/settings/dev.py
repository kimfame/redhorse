from .base import *

DEBUG = False

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS += [
    env("DEV_BACKEND_DOMAIN"),
]


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}


# CORS

CORS_ALLOWED_ORIGINS = [
    f"https://{env('DEV_FRONTEND_DOMAIN')}",
]


# Admin URL

ADMIN_URL = env("ADMIN_URL")
