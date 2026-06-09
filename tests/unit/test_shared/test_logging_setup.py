"""Tests for logging initialisation (namespace, dir creation, dictConfig)."""

from __future__ import annotations

import json
import logging

from cosmos77_ex03.shared.logging_setup import (
    _ensure_handler_dirs,
    get_logger,
    init_logging,
)


def test_get_logger_namespace():
    assert get_logger().name == "cosmos77_ex03"
    assert get_logger("cosmos77_ex03.crew").name == "cosmos77_ex03.crew"


def test_ensure_handler_dirs_creates(tmp_path):
    payload = {
        "handlers": {
            "f": {"filename": str(tmp_path / "a" / "b.log")},
            "d": {"directory": str(tmp_path / "c")},
            "console": {"class": "logging.StreamHandler"},
        }
    }
    _ensure_handler_dirs(payload)
    assert (tmp_path / "a").is_dir()
    assert (tmp_path / "c").is_dir()


def test_init_logging_applies_dictconfig(tmp_path):
    cfgfile = tmp_path / "logging.json"
    cfgfile.write_text(
        json.dumps(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {"s": {"format": "%(message)s"}},
                "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "s"}},
                "loggers": {"cosmos77_ex03": {"level": "DEBUG", "handlers": ["console"]}},
            }
        )
    )
    init_logging(cfgfile)
    assert logging.getLogger("cosmos77_ex03").level == logging.DEBUG
