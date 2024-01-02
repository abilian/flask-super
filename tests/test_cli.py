import pytest
import svcs
from click.testing import CliRunner
from flask import Flask

from flask_super.decorators import service
from flask_super.scanner import scan_package
from flask_super.services import register_services


@service
class ServiceClass:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)

    return app


@pytest.mark.skip()
def test_cli():
    scan_package("flask_super.cli.commands")

    app = create_app()
    register_services(app)

    runner = CliRunner()
    result = runner.invoke(app.cli, ["inspect"])
    print(result.output)
    assert result.exit_code == 0
