import environ
import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Env

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "phone",
    "option_code",
    "user_profile",
    "user",
    "profile_picture",
    "match",
    "chat_room",
    "chat_message",
    "feed",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "redhorse.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "redhorse.wsgi.application"


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = False
USE_TZ = False
DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i:s"


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Red Horse settings (Minimum time unit : minute)

MAX_LIKE_NUM = env("MAX_LIKE_NUM", default=5)
MAX_PASSION_NUM = env("MAX_PASSION_NUM", default=3)
MAX_PROFILE_PICTURE_NUM = env("MAX_PROFILE_PICTURE_NUM", default=9)
PASSWORD_RESET_RETRY_WAIT_TIME = env("PASSWORD_RESET_RETRY_WAIT_TIME", default=10)
VERIFICATION_CODE_EXP_TIME = env("VERIFICATION_CODE_EXP_TIME", default=3)
VERIFIED_PHONE_NUMBER_EXP_TIME = env("VERIFIED_PHONE_NUMBER_EXP_TIME", default=60)
