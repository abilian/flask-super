import pytest
import svcs
from flask import Flask
from flask.testing import FlaskCliRunner


@pytest.fixture()
def app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)
    return app


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
