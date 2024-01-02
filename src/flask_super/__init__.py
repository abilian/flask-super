"""Top-level package for Flask-Super."""

from __future__ import annotations

from flask_super.cli import register_commands


def init_app(app):
    register_commands(app)
    return app
