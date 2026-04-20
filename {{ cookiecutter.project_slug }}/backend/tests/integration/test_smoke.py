"""Integration tests: Django DB, views, and HTTP client (no real browser)."""

import pytest
from django.urls import reverse

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_home(client) -> None:
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200


{% if cookiecutter.use_i18n == "y" %}
def test_i18n_set_language_url() -> None:
    assert reverse("set_language") == "/i18n/setlang/"


{% endif %}
{% if cookiecutter.api_project == "y" %}
@pytest.mark.django_db
def test_api_health(client) -> None:
    url = reverse("api-v1-health")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


{% if cookiecutter.openapi_schema == "drf-spectacular" %}
@pytest.mark.django_db
def test_openapi_schema_spectacular(client) -> None:
    url = reverse("api-schema")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_redoc_endpoint(client) -> None:
    url = reverse("api-redoc")
    response = client.get(url)
    assert response.status_code == 200
{% elif cookiecutter.openapi_schema == "drf-yasg" %}
@pytest.mark.django_db
def test_openapi_schema_yasg_json(client) -> None:
    url = reverse("api-schema-openapi", kwargs={"format": "json"})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_redoc_endpoint(client) -> None:
    url = reverse("api-schema-redoc")
    response = client.get(url)
    assert response.status_code == 200
{% endif %}
{% endif %}
