import click
from yaml import scan

from flask_plus.registry import lookup, register

__all__ = ["register_commands", "command", "group"]


def command(*args, **kwargs):
    def decorator(func):
        module = func.__module__
        name = func.__name__
        cmd = click.command(*args, **kwargs)(func)
        register(cmd, name=name, module=module, tags=["cli"])
        return cmd

    return decorator


def group(*args, **kwargs):
    def decorator(func):
        module = func.__module__
        name = func.__name__
        cmd = click.group(*args, **kwargs)(func)
        register(cmd, name=name, module=module, tags=["cli"])
        return cmd

    return decorator


def register_commands(app):
    scan(app, "flask_plus.cli.commands")

    for obj in lookup(click.Command):
        app.cli.add_command(obj)
