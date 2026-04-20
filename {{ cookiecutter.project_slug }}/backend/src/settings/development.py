"""Development settings — debug on, safe defaults for engineers and CI dev jobs."""

from .base import *  # noqa: F403

DEBUG = env.get_bool("DJANGO_DEBUG", default=True, required=False)  # noqa: F405

EMAIL_BACKEND = env.get_str(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
    required=False,
)  # noqa: F405

{% if cookiecutter['__frontend_framework'] in ["vue", "react"] %}
DJANGO_VITE["default"]["dev_mode"] = True  # noqa: F405
{% endif %}
