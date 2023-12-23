import pytest
import svcs
from click.testing import CliRunner
from flask import Flask

from flask_plus.decorators import service
from flask_plus.scanner import scan_package
from flask_plus.services import register_services


@service
class ServiceClass:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)

    return app


def test_cli():
    scan_package("flask_plus.cli.commands")

    app = create_app()
    register_services(app)

    runner = CliRunner()
    result = runner.invoke(app.cli, ["inspect"])
    print(result.output)
    assert result.exit_code == 0
