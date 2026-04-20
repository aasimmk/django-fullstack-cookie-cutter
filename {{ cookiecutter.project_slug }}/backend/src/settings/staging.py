"""Staging / pre-production — production-like, tuned for a non-live environment."""

from .base import *  # noqa: F403

DEBUG = env.get_bool("DJANGO_DEBUG", default=False, required=False)  # noqa: F405
SECRET_KEY = env.get_str("DJANGO_SECRET_KEY", required=True)  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = env.get_bool(
    "DJANGO_SESSION_COOKIE_SECURE",
    default=True,
    required=False,
)  # noqa: F405
CSRF_COOKIE_SECURE = env.get_bool(
    "DJANGO_CSRF_COOKIE_SECURE",
    default=True,
    required=False,
)  # noqa: F405
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Enable HSTS only once you are sure all staging traffic is HTTPS-only.
SECURE_HSTS_SECONDS = env.get_int(
    "DJANGO_SECURE_HSTS_SECONDS",
    default=0,
    required=False,
)  # noqa: F405
if SECURE_HSTS_SECONDS:
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

{% if cookiecutter.frontend_framework in ["vue", "react"] %}
DJANGO_VITE["default"]["dev_mode"] = False  # noqa: F405
{% endif %}

{% if cookiecutter.api_project == "y" %}
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]
{% endif %}
