"""Production settings — import via DJANGO_SETTINGS_MODULE."""

from .base import *  # noqa: F403

DEBUG = env.get_bool("DJANGO_DEBUG", default=False, required=False)  # noqa: F405
SECRET_KEY = env.get_str("DJANGO_SECRET_KEY", required=True)  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
DJANGO_VITE["default"]["dev_mode"] = False  # noqa: F405
{% endif %}

{% if cookiecutter.api_project == "y" %}
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]
{% endif %}
