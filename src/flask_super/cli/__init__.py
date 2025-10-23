from __future__ import annotations

from typing import Any
from collections.abc import Callable

import click

from flask_super.registry import lookup, register

__all__ = ["command", "group", "register_commands"]

from flask_super.scanner import scan_package


def command(*args: Any, **kwargs: Any) -> Callable:
    def decorator(func: Callable) -> click.Command:
        module = func.__module__
        name = func.__name__
        cmd = click.command(*args, **kwargs)(func)
        register(cmd, name=name, module=module, tag="cli")
        return cmd

    return decorator


def group(*args: Any, **kwargs: Any) -> Callable:
    def decorator(func: Callable) -> click.Group:
        module = func.__module__
        name = func.__name__
        cmd = click.group(*args, **kwargs)(func)
        register(cmd, name=name, module=module, tag="cli")
        return cmd

    return decorator


def register_commands(app):
    scan_package("flask_super.cli.commands")

    for obj in lookup(click.Command):
        app.cli.add_command(obj)
