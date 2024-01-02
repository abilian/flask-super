from __future__ import annotations

import click

from flask_super.registry import lookup, register

__all__ = ["register_commands", "command", "group"]

from flask_super.scanner import scan_package


def command(*args, **kwargs):
    def decorator(func):
        module = func.__module__
        name = func.__name__
        cmd = click.command(*args, **kwargs)(func)
        register(cmd, name=name, module=module, tag="cli")
        return cmd

    return decorator


def group(*args, **kwargs):
    def decorator(func):
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
