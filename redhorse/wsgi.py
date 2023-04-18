import os

from django.core.wsgi import get_wsgi_application
from redhorse.settings.base import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"redhorse.settings.{env('ENV_MODE')}")

application = get_wsgi_application()
