import pytest
import svcs
from flask import Flask
from flask.testing import FlaskCliRunner


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    return svcs.flask.init_app(app)


@pytest.fixture
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
