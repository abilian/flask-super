import nox

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13`"]
DEFAULT_PYTHON_VERSION = PYTHON_VERSIONS[-1]
nox.options.sessions = ["lint", "pytest"]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session: nox.Session) -> None:
    session.run("uv", "sync")
    session.run("uv", "pip", "check")
    session.run("uv", "run", "make", "lint")
    session.run("uv", "pip", "install", "safety", "pip-audit")
    session.run("uv", "run", "adt", "audit")


@nox.session(python=PYTHON_VERSIONS)
def pytest(session: nox.Session) -> None:
    session.run("uv", "sync")
    session.run("uv", "run", "pytest", "--tb=short")
