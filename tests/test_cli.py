import svcs
from click.testing import CliRunner
from flask import Flask

from flask_plus.decorators import service


@service
class ServiceClass:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)

    return app


def test_cli():
    app = create_app()
    runner = CliRunner()
    result = runner.invoke(app.cli, ["inspect"])
    debug(result.output)
    assert result.exit_code == 0
