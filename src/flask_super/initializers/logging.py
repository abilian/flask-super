# ruff: noqa: PLC0415

from __future__ import annotations

import logging
import sys

from flask import Flask
from loguru import logger


def init_logging(app: Flask) -> None:
    run_from_cli = app.config.get("RUN_FROM_CLI")
    if run_from_cli and not app.debug:
        print("Running from CLI, skipping logging init (use --debug to enable)")
        logger.configure(handlers=[])
    else:
        init_loguru(app)
        init_sentry(app)


class InterceptHandler(logging.Handler):
    def emit(self, record):  # noqa: PLR6301
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def init_loguru(app: Flask):
    """Register loguru as (sole) handler."""
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

    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(dsn=dsn, integrations=[FlaskIntegration()])
