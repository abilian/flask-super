from devtools import debug
from flask import Flask
from flask.testing import FlaskCliRunner

import flask_super
from flask_super.decorators import service
from flask_super.scanner import scan_package
from flask_super.services import register_services


@service
class ServiceClass:
    pass


def test_cli(app: Flask, runner: FlaskCliRunner):
    scan_package("flask_super.cli.commands")
    register_services(app)
    flask_super.init_app(app)

    result = runner.invoke(args=["inspect"])
    debug(result.output)
    assert result.exit_code == 0
