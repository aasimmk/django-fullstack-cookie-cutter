"""Test settings — isolated SQLite DB for pytest (no Postgres required)."""

from .base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

{% if cookiecutter.use_redis_cache == "y" %}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "pytest-cache",
    },
}
{% endif %}
