"""Tests for the version constant + config-version validation."""

from __future__ import annotations

import pytest

from cosmos77_ex03.shared.version import VERSION, validate_config_version


def test_version_is_one_zero():
    assert VERSION == "1.00"


def test_validate_accepts_matching():
    validate_config_version("1.00")  # must not raise


def test_validate_rejects_mismatch():
    with pytest.raises(ValueError, match="does not match"):
        validate_config_version("0.99")
