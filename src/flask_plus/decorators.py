from .cli import command, group
from .registry import register

__all__ = ["register", "command", "group", "service"]


def service(cls):
    return register(cls, tag="service")
