# Flask-Super

[![image](https://img.shields.io/pypi/v/flask_super.svg)](https://pypi.python.org/pypi/flask_super)

[![Documentation Status](https://readthedocs.org/projects/flask-super/badge/?version=latest)](https://flask-super.readthedocs.io/en/latest/?version=latest)

> "Any sufficiently complicated Python program contains an ad-hoc, informally-specified
> bug-ridden slow implementation of half of the Zope Component Architecture." (S. Fermigier, December 2023).


> [!WARNING]
> Due to PyPI refusing the submission of a package called "FLask-Plus", the package
> has been renamed (temporarily?) "Flask-Super".
>
> (I know this sucks. Either way, it's temporary. Stay tuned.)


## Flask patterns and idoms

-   Free software: Apache Software License 2.0


## Features

- Decorator-based registration system for services (using [svcs](https://svcs.hynek.me/))
- Powerful inspection CLI command (`flask inspect` and `flask config`).
- Flask initialisation helpers.


## Status

This is a preview. Expect the API to change.

## Sample usage

```python

import svcs
from flask import Flask
from flask_super import register_services
from flask_super.scanner import scan_package

# Assuming you have developped the proper decorators and registration logic
# in app.lib (or any other module)
from app.lib import register_routes, register_components


def create_app():
    app = Flask(__name__)

    svcs.flask.init_app(app)
    scan_package("app.services")
    register_services(app)

    # Or just scan a package if using a framework like SQLAlchemy which
    # automatically registers classes on import
    scan_package("app.models")

    # You may also scan custom things (e.g. models, routes, components, etc.)
    scan_package("app.routes")
    register_routes(app)
    scan_package("app.components")
    register_components(app)

    return app


app = create_app()
```

Currently, `flask-super` provides the following decorators:

- `@service`: register a service with a per-request lifecycle (on the `svcs` registry)
- `@singleton`: register a singleton service (on the `svcs` registry)


## A real-life example

Here is the initialisation code of a Flask application using `flask-super`:

```python
def create_app(config: Any = None) -> Flask:
    # When testing
    if config:
        app = Flask(__name__)
        app.config.from_object(config)

    # Otherwise
    else:
        # Not needed when called from CLI, but needed when
        # called from a WSGI server
        load_dotenv(verbose=True)

        app = Flask(__name__)
        app.config.from_prefixed_env()

        finish_config(app)

    init_app(app)
    return app


def finish_config(app: Flask):
    app.config.from_object("app.config.Config")


def init_app(app: Flask):
    # First: Logging & Observability (e.g. sentry)
    init_logging(app)

    # Scan modules that may provide side effects
    scan_package("app.models")
    scan_package("app.services")
    scan_package("app.controllers")
    scan_package("app.cli")

    # Scan 3rd-party modules
    scan_package("flask_super")

    # Extensions, then services
    init_extensions(app)
    svcs.flask.init_app(app)
    register_services(app)

    # Web
    register_views(app)
    register_controllers(app)

    # Security
    register_rules()

    # CLI
    register_commands(app)
```

## Credits

This package was created with [Cruft](https://cruft.github.io/cruft/)
and the
[abilian/cookiecutter-abilian-python](https://github.com/abilian/cookiecutter-abilian-python)
project template.
