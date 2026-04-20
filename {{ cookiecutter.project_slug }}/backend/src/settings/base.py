"""Base Django settings — shared across environments."""

from pathlib import Path

from ._env import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = env.get_str(
    "DJANGO_SECRET_KEY",
    default="change-me-in-production-not-for-deployment",
    required=False,
)

ALLOWED_HOSTS: list[str] = env.get_list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1"],
    required=False,
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "guardian",
    "waffle",
    {% if cookiecutter.frontend_framework == "htmx" %}"django_htmx",{% endif %}
    {% if cookiecutter.frontend_framework in ["vue", "react"] %}"django_vite",{% endif %}
    "src.apps.users",
    {% if cookiecutter.use_celery == "y" %}
    "django_celery_beat",
    "src.apps.tasks",
    {% endif %}
    {% if cookiecutter.api_project == "y" %}
    "rest_framework",
    {% if cookiecutter.openapi_schema == "drf-spectacular" %}
    "drf_spectacular",
    {% elif cookiecutter.openapi_schema == "drf-yasg" %}
    "drf_yasg",
    {% endif %}
    "django_filters",
    "corsheaders",
    "src.apps.api",
    {% endif %}
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    {% if cookiecutter.api_project == "y" %}
    "corsheaders.middleware.CorsMiddleware",
    {% endif %}
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    {% if cookiecutter.use_i18n == "y" %}
    "django.middleware.locale.LocaleMiddleware",
    {% endif %}
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "waffle.middleware.WaffleMiddleware",
    {% if cookiecutter.frontend_framework == "htmx" %}"django_htmx.middleware.HtmxMiddleware",{% endif %}
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                {% if cookiecutter.use_i18n == "y" %}
                "django.template.context_processors.i18n",
                {% endif %}
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"
ASGI_APPLICATION = "src.asgi.application"

{% if cookiecutter.use_postgresql == "y" %}
import environ as django_environ

DATABASES = {
    "default": django_environ.Env().db(
        "DATABASE_URL",
        default="postgres://{{ cookiecutter.project_slug }}:{{ cookiecutter.project_slug }}@localhost:5432/{{ cookiecutter.project_slug }}",
    )
}
{% else %}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
{% endif %}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = {% if cookiecutter.use_i18n == "y" %}True{% else %}False{% endif %}
USE_TZ = True
{% if cookiecutter.use_i18n != "y" and cookiecutter.django_version == "4.2" %}
USE_L10N = False
{% endif %}
{% if cookiecutter.use_i18n == "y" %}
LANGUAGES = [
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
{% endif %}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = []
{% if cookiecutter.frontend_framework in ["vue", "react"] %}
STATICFILES_DIRS.append(BASE_DIR / "static" / "dist")
{% endif %}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

{% if cookiecutter.frontend_framework in ["vue", "react"] %}
DJANGO_VITE = {
    "default": {
        "dev_mode": env.get_bool("DJANGO_VITE_DEV_MODE", default=False, required=False),
        "manifest_path": BASE_DIR / "static" / "dist" / ".vite" / "manifest.json",
    },
}
{% endif %}

{% if cookiecutter.api_project == "y" %}
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    {% if cookiecutter.openapi_schema == "drf-spectacular" %}
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    {% else %}
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    {% endif %}
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
{% if cookiecutter.openapi_schema == "drf-spectacular" %}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_slug }} API",
    "DESCRIPTION": "OpenAPI 3 schema",
    "VERSION": "1.0.0",
}
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
SWAGGER_USE_COMPAT_RENDERERS = False
{% endif %}

CORS_ALLOWED_ORIGINS = env.get_list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        {% if cookiecutter.frontend_framework in ["vue", "react"] %}
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        {% elif cookiecutter.frontend_framework in ["nuxt", "next"] %}
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        {% endif %}
    ],
    required=False,
)
CORS_ALLOW_CREDENTIALS = True
{% endif %}

{% if cookiecutter.use_redis_cache == "y" %}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.get_str(
            "REDIS_CACHE_URL",
            default="redis://127.0.0.1:6379/0",
            required=False,
        ),
    },
}
{% endif %}

{% if cookiecutter.use_celery == "y" %}
{% if cookiecutter.celery_broker == "rabbitmq" %}
CELERY_BROKER_URL = env.get_str(
    "CELERY_BROKER_URL",
    default="amqp://guest:guest@localhost:5672//",
    required=False,
)
CELERY_RESULT_BACKEND = env.get_str(
    "CELERY_RESULT_BACKEND",
    default="rpc://",
    required=False,
)
{% else %}
CELERY_BROKER_URL = env.get_str(
    "CELERY_BROKER_URL",
    default="redis://localhost:6379/0",
    required=False,
)
CELERY_RESULT_BACKEND = env.get_str(
    "CELERY_RESULT_BACKEND",
    default="redis://localhost:6379/1",
    required=False,
)
{% endif %}
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
{% endif %}
