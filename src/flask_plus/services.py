from __future__ import annotations

from inspect import signature

import svcs
from flask import Flask
from svcs.flask import register_factory

__all__ = [
    "register_services",
]

from flask_plus.registry import lookup


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
            cls = sig.return_annotation
            svcs.flask.register_factory(app, cls, factory)
