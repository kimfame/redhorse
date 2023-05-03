import os

from django.core.asgi import get_asgi_application

from redhorse.settings.base import env


os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"redhorse.settings.{env('ENV_MODE')}")

application = get_asgi_application()
