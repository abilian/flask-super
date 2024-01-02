import svcs
from flask import Flask
from svcs.flask import container

from flask_super.decorators import service, singleton
from flask_super.services import register_services, register_singletons


def create_app() -> Flask:
    app = Flask(__name__)
    app = svcs.flask.init_app(app)
    return app


def test_single_service():
    @service
    class ServiceClass:
        pass

    app = create_app()
    register_services(app)

    with app.app_context():
        svc = container.get(ServiceClass)
        assert svc is not None
        assert isinstance(svc, ServiceClass)

        # The service is unique over a single request.
        svc2 = container.get(ServiceClass)
        assert svc2 == svc

    with app.app_context():
        svc3 = container.get(ServiceClass)
        assert svc3 != svc


def test_singleton():
    """Test that a singleton service is only created once over the lifetime
    of an application."""

    @singleton
    class Singleton:
        pass

    app = create_app()
    register_singletons(app)

    with app.app_context():
        svc1 = container.get(Singleton)
        svc2 = container.get(Singleton)
        assert svc1 is svc2

    with app.app_context():
        svc3 = container.get(Singleton)
        assert svc3 == svc1
