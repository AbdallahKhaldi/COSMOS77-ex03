"""Phase-0 smoke test: the package imports and core constants are sane."""

from __future__ import annotations

import cosmos77_ex03
from cosmos77_ex03 import constants


def test_package_version_is_one_zero():
    assert cosmos77_ex03.__version__ == "1.00"


def test_default_encoding_is_utf8():
    assert constants.DEFAULT_ENCODING == "utf-8"


def test_package_name_matches_module():
    assert constants.PACKAGE_NAME == "cosmos77_ex03"


def test_project_version_matches_package():
    assert constants.PROJECT_VERSION == cosmos77_ex03.__version__
