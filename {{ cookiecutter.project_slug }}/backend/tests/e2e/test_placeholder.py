"""End-to-end tests: real HTTP server (``live_server``) or external automation."""

import urllib.request

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.django_db]


def test_placeholder_live_server_home(live_server) -> None:
    """Replace or extend with browser automation (Playwright/Selenium) as needed."""
    url = f"{live_server.url}/"
    with urllib.request.urlopen(url, timeout=5) as response:
        assert response.getcode() == 200
