"""Top-level package for Flask-Super."""

from __future__ import annotations

from flask_super.cli import register_commands
from flask_super.scanner import scan_package
from flask_super.services import register_services

__all__ = ["init_app", "register_services", "scan_package", "register_commands"]


def init_app(app):
    register_services(app)

    scan_package("flask_super.cli.commands")
    register_commands(app)

    return app
