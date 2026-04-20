"""Versioned HTTP API routes."""

{% if cookiecutter.openapi_schema == "drf-yasg" %}
from django.urls import path, re_path
{% else %}
from django.urls import path
{% endif %}
{% if cookiecutter.openapi_schema == "drf-spectacular" %}
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
{% endif %}

from .views import HealthAPIView

urlpatterns = [
    path("v1/health/", HealthAPIView.as_view(), name="api-v1-health"),
]

{% if cookiecutter.openapi_schema == "drf-spectacular" %}
urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-schema-swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-schema-redoc",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
]
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
schema_view = get_schema_view(
    openapi.Info(
        title="{{ cookiecutter.project_slug }} API",
        default_version="v1",
        description="OpenAPI 2.0 schema (Swagger).",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(
        r"^swagger\.(?P<format>json|yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="api-schema-openapi",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="api-schema-redoc",
    ),
]
{% endif %}
