"""ASGI config for {{ cookiecutter.project_name }}."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings.production")

application = get_asgi_application()
