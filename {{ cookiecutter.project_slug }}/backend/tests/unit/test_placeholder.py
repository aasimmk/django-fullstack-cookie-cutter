"""Fast unit tests: pure Python or isolated helpers (no Django DB)."""

import pytest

pytestmark = pytest.mark.unit


def test_placeholder_unit_workspace() -> None:
    assert True
