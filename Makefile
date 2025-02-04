.PHONY: all develop test lint clean doc format
.PHONY: clean clean-build clean-pyc clean-test coverage dist docs install lint lint/flake8

# The package name
PKG=flask_super

all: test lint

#
# Setup
#

## Install development dependencies and pre-commit hook (env must be already activated)
develop: install-deps activate-pre-commit configure-git

install-deps:
	@echo "--> Installing dependencies"
	uv sync

activate-pre-commit:
	@echo "--> Activating pre-commit hook"
	pre-commit install

configure-git:
	@echo "--> Configuring git"
	git config branch.autosetuprebase always


#
# testing & checking
#
.PHONY: test test-randomly test-with-coverage test-with-typeguard clean-test lint audit

## Run python tests
test:
	@echo "--> Running Python tests"
	pytest --ff -x -p no:randomly
	@echo ""

test-randomly:
	@echo "--> Running Python tests in random order"
	pytest
	@echo ""

test-with-coverage:
	@echo "--> Running Python tests"
	py.test --cov $(PKG)
	@echo ""

test-with-typeguard:
	@echo "--> Running Python tests with typeguard"
	pytest --typeguard-packages=${PKG}
	@echo ""

## Cleanup tests artifacts
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

## Lint / check typing
lint:
	adt check src tests
	pyanalyze src tests

# Alt
#lint:
#	ruff src tests/test*.py
#	mypy --show-error-codes src
#	flake8 src tests/test*.py
#	# python -m pyanalyze --config-file pyproject.toml src
#	lint-imports
#	make hadolint
#	vulture --min-confidence 80 src
#	deptry . --extend-exclude .nox --extend-exclude .tox
#	# TODO later
#	# mypy --check-untyped-defs src


## Run a security audit
audit:
	pip-audit
	safety check


#
# Formatting
#
.PHONY: format

## Format / beautify code
format:
	docformatter -i -r src
	black src
	isort src tests


#
# Everything else
#
.PHONY: help install doc doc-html doc-pdf clean tidy update-deps publish

help:
	@inv help-make

install:
	uv sync

doc: doc-html doc-pdf

doc-html:
	sphinx-build -W -b html docs/ docs/_build/html

doc-pdf:
	sphinx-build -W -b latex docs/ docs/_build/latex
	make -C docs/_build/latex all-pdf

## Cleanup repository
clean:
	rm -f **/*.pyc
	find . -type d -empty -delete
	rm -rf *.egg-info *.egg .coverage .eggs .cache .mypy_cache .pyre \
		.pytest_cache .pytest .DS_Store  docs/_build docs/cache docs/tmp \
		dist build pip-wheel-metadata junit-*.xml htmlcov coverage.xml

## Cleanup harder
tidy: clean
	rm -rf .nox
	rm -rf node_modules
	rm -rf instance

## Update dependencies
update-deps:
	uv sync -U
	pre-commit autoupdate
	uv pip list --outdated

## Publish to PyPI
publish: clean
	git push
	git push --tags
	uv build
	twine upload dist/*
