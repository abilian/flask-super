from __future__ import annotations

import importlib
from inspect import signature
from typing import Any

import svcs
from attr import field, frozen
from flask import Flask
from svcs.flask import register_factory

__all__ = [
    "register_services",
]

from flask_super.registry import lookup


def register_services(app: Flask):
    services = lookup(tag="service")

    for cls_or_factory in services:
        if factory := getattr(cls_or_factory, "svcs_factory", None):
            register_factory(app, cls_or_factory, factory)

        elif isinstance(cls_or_factory, type):
            cls = cls_or_factory
            svcs.flask.register_factory(app, cls, cls)

        else:
            factory = cls_or_factory
            sig = signature(factory)
            cls_name = sig.return_annotation
            module = importlib.import_module(factory.__module__)
            cls = getattr(module, cls_name)
            svcs.flask.register_factory(app, cls, factory)


@frozen
class SingletonFactory:
    cls: type
    holder: list[Any] = field(factory=list)

    def __call__(self) -> Any:
        if not self.holder:
            self.holder.append(self.cls())
        return self.holder[0]


def register_singletons(app: Flask):
    singletons = lookup(tag="singleton")

    for cls in singletons:
        svcs.flask.register_factory(app, cls, SingletonFactory(cls))
