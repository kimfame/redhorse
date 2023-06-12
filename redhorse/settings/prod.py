from datetime import timedelta

from .base import *


DEBUG = False

SECRET_KEY = env("SECRET_KEY")


# Database

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
}


# Simple JWT

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=28),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": env("SIGNING_KEY"),
}


# Pusher

PUSHER_APP_ID = env("PUSHER_APP_ID")
PUSHER_KEY = env("PUSHER_KEY")
PUSHER_SECRET = env("PUSHER_SECRET")
PUSHER_CLUSTER = env("PUSHER_CLUSTER")
PUSHER_SSL = True


# Admin URL

ADMIN_URL = env("ADMIN_URL")


# Secure settings

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 365 * 24 * 60 * 60
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "custom_formatter": {
            "format": "{asctime}.{msecs:0<3.0f} [{levelname:^8}][{name}] {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "custom_formatter",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "scripts": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "core": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}

for app in PROJECT_APPS:
    LOGGING["loggers"][app.split(".")[0]] = {
        "handlers": ["console", "file"],
        "level": "INFO",
    }
