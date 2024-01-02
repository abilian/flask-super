from __future__ import annotations

from cleez.colors import blue
from flask.cli import with_appcontext
from svcs.flask import container

from flask_super.cli import command
from flask_super.registry import registry


@command(short_help="Inspect app")
@with_appcontext
def inspect():
    inspect_registry()
    inspect_services()


def inspect_registry():
    print(blue("\nRegistry:"))
    print()

    def sorter(t):
        _, metadata = t
        return metadata.tag, metadata.name

    objs = sorted(registry.items(), key=sorter)

    rows = []
    for obj, metadata in objs:
        name = metadata.name
        module = metadata.module
        tag = metadata.tag
        obj_type = str(type(obj))
        rows.append((name, obj_type, tag, module))

    headers = ["Obj", "Type", "Tag", "Module"]
    print_table(headers, rows)


def inspect_services():
    print(blue("\nServices:"))
    print()

    registry = container.registry
    services = [
        (registered_service.svc_type.__name__, registered_service.factory)
        for registered_service in registry._services.values()
    ]
    services.sort(key=lambda x: x[0].lower())

    rows = []
    for k, _v in services:
        if hasattr(_v, "cls"):
            v = _v.cls  # type: ignore
        else:
            v = _v

        name = v.__name__
        module = v.__module__
        rows.append((k, name, module))

    headers = ["Type", "Factory", "Module"]
    print_table(headers, rows)


def print_table(headers, rows):
    rows.insert(0, headers)
    widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    rows.insert(1, ["-" * w for w in widths])
    template = "  ".join(f"{{{i}:<{w}}}" for i, w in enumerate(widths))

    for row in rows:
        print(template.format(*row))
    print()
