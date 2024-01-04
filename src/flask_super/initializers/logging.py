from __future__ import annotations

import logging
import os
import sys

from flask import Flask
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def init_logging(app: Flask) -> None:
    run_from_cli = app.config.get("RUN_FROM_CLI")
    if run_from_cli and not app.debug:
        print("Running from CLI, skipping logging init (use --debug to enable)")
        logger.configure(handlers=[])
    else:
        init_loguru(app)
        init_sentry(app)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def init_loguru(app: Flask):
    """Register loguru as (sole) handler"""
    if app.debug:
        level = "DEBUG"
    else:
        level = "INFO"

    logger.remove()
    logger.add(sys.stderr, level=level)

    app.logger.handlers = [InterceptHandler()]
    logger.info("Loguru initialized")


def init_sentry(app: Flask) -> None:
    dsn = app.config.get("SENTRY_DSN")
    if not dsn:
        return

    release = os.environ.get("VERSION")
    sentry_sdk.init(dsn=dsn, integrations=[FlaskIntegration()], release=release)

    @app.before_request
    def sentry_event_context() -> None:
        # TODO
        pass
        # if request.data:
        #     order = json.loads(request.data)
        #     with sentry_sdk.configure_scope() as scope:
        #         scope.user = { "email" : order["email"] }
        #
        # transactionId = request.headers.get('X-Transaction-ID')
        # sessionId = request.headers.get('X-Session-ID')
        #
        # with sentry_sdk.configure_scope() as scope:
        #     scope.set_tag("transaction_id", transactionId)
        #     scope.set_tag("session-id", sessionId)
