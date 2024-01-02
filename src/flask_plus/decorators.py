from __future__ import annotations

from .cli import command, group
from .registry import register

__all__ = ["register", "command", "group", "service"]


def service(obj):
    return register(obj, tag="service")


def singleton(obj):
    return register(obj, tag="singleton")
