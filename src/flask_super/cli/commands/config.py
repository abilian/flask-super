from __future__ import annotations

import os

from cleez.colors import blue
from flask import current_app
from flask.cli import with_appcontext

from flask_super.cli import command


@command(short_help="Show config")
@with_appcontext
def config() -> None:
    print(blue("CONFIG:\n"))
    print_config()

    print(blue("\nENV:\n"))
    print_env()


def print_env():
    env_ = dict(sorted(os.environ.items()))
    for k, v in env_.items():
        print(f"{k}: {v}")


def print_config():
    config_ = dict(sorted(current_app.config.items()))
    for k, v in config_.items():
        try:
            v_str = str(v)
        except Exception:  # noqa: BLE001
            v_str = repr(v)
        print(f"{k}: {v_str}")
