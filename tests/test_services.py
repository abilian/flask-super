import svcs
from flask import Flask
from svcs.flask import container

from flask_plus.decorators import service


@service
class ServiceClass:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)

    return app


def test_1():
    app = create_app()
    with app.app_context():
        svc = container.get(ServiceClass)
        assert svc is not None
        assert isinstance(svc, ServiceClass)
