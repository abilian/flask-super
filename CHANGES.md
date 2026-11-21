# Changes

## 0.2.13 (2026-11-21)

- Declare `attrs` and `termcolor` as dependencies. The package imports them but did not list them, so a clean install could fail.
- Add `typing-extensions` as a dependency.
- `lookup()` now raises `AssertionError` (via `assert_never`) instead of `TypeError` when given a key that is neither a string nor a type.
- `flask inspect` no longer crashes on services registered under a type form without a `__name__` (e.g. `Annotated[...]`).
- Fix errors reported by pyrefly, ty and zuban.

## 0.2.12 (2025-10-28)

- Move type-only imports under `TYPE_CHECKING`.
- Code cleanup.

## 0.2.11 (2025-10-23)

- Add type annotations to the `@command` and `@group` decorators.
- Logging initialisation: only treat `app.debug` as debug mode when it is exactly `True`.
- Update dependencies.

## 0.2.10 (2025-04-07)

- Remove the dependency on `cleez`; terminal colours now use `termcolor`.
- `flask config` no longer shows dunder keys.
- Switch from Poetry to uv for packaging and development.
- CI updates.

## 0.2.8 (2024-07-04)

- Documentation updates.
- Update dependencies and ruff configuration.

## 0.2.7 (2024-05-01)

- Update dependencies.

## 0.2.6 (2024-02-01)

- Update dependencies.

## 0.2.5 (2024-01-19)

- `scan_packages()` now accepts any iterable of package names and rejects a single string passed by mistake.
- Add usage hints to the documentation.
- Lock dependencies.

## 0.2.4 (2024-01-04)

- Fix a type annotation in `scan_packages()`.
- `init_logging` can be imported from `flask_super.initializers`.

## 0.2.3 (2024-01-04)

- Add logging initialisation helpers.
- Import `sentry-sdk` lazily.

## 0.2.2 (2024-01-03)

- Clean up and improve `init_app`.
- Use `attrs.frozen` instead of `attrs.define`.

## 0.2.1 (2024-01-03)

- Add the `flask config` command.

## 0.2.0 (2024-01-02)

- Cleanup and test fixes.

## 0.1.1 (2023-12-23)

- Initial release: registry, package scanner, CLI command registration and `@singleton` support.
