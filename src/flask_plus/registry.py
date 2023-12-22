from typing import Any

from attr import define, field

__all__ = ["registry", "register", "lookup"]


@define
class Metadata:
    name: str = ""
    module: str = ""
    tags: list[str] = field(factory=list)
    extras: dict[str, Any] = field(factory=dict)


@define
class Registry:
    registered: dict[Any, Metadata] = field(factory=dict)

    def register(self, obj, name=None, module=None, tag=None, tags=None, extras=None):
        if name is None:
            name = obj.__name__
        if module is None:
            module = obj.__module__

        if tag:
            tags = [tag]
        elif tags is None:
            tags = []

        if extras is None:
            extras = {}

        metadata = Metadata(name=name, module=module, tags=tags, extras=extras)
        self.registered[obj] = metadata
        return obj

    def lookup(self, key: str | type = "", tag: str = "") -> list:
        match key:
            case "":
                objs = list(self.registered.items())
            case str():
                objs = self._lookup_by_name(key)
            case type():
                objs = self._lookup_by_type(key)
            case _:
                raise TypeError(f"Invalid key type: {type(key)}")

        if tag:
            return [obj for obj, metadata in objs if tag in metadata.tags]
        else:
            return [obj for obj, _metadata in objs]

    def _lookup_by_name(self, name: str) -> list:
        result = []
        for obj, metadata in self.registered.items():
            if metadata.name == name:
                result.append((obj, metadata))
        return result

    def _lookup_by_type(self, cls: type) -> Any:
        result = []
        for obj, metadata in self.registered.items():
            if isinstance(obj, type):
                if issubclass(obj, cls):
                    result.append((obj, metadata))
            elif isinstance(obj, cls):
                result.append((obj, metadata))

        return result

    def __iter__(self):
        return iter(self.registered)

    def items(self):
        return self.registered.items()

    def __contains__(self, obj):
        return obj in self.registered

    def get_metadata(self, obj: Any) -> Metadata:
        return self.registered[obj]

    def clear(self):
        self.registered.clear()


registry = Registry()
register = registry.register
lookup = registry.lookup
