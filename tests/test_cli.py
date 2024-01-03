from flask import Flask
from flask.testing import FlaskCliRunner

import flask_super
from flask_super.decorators import service


@service
class ServiceClass:
    pass


def test_cli(app: Flask, runner: FlaskCliRunner):
    flask_super.init_app(app)

    result = runner.invoke()
    assert "inspect" in result.output
    assert "config" in result.output

    result = runner.invoke(args=["inspect"])
    assert "ServiceClass" in result.output

    result = runner.invoke(args=["config"])
    assert "CONFIG:" in result.output
