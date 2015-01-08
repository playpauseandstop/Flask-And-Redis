.PHONY: bootstrap clean distclean pep8 server shell test

# Project and environment settings
APP = flask_redis
PROJECT = .

ENV ?= env
VENV = $(shell python -c 'import sys; print(int(hasattr(sys, "real_prefix")));')

ifeq ($(VENV),1)
	IPYTHON = PYTHONPATH=.:.. ipython
	NOSETESTS = PYTHONPATH=.:.. nosetests
	PEP8 = flake8
	PYTHON = PYTHONPATH=.:.. python
else
	IPYTHON = PYTHONPATH=.:.. $(ENV)/bin/ipython
	NOSETESTS = PYTHONPATH=.:.. $(ENV)/bin/nosetests
	PEP8 = $(ENV)/bin/flake8
	PYTHON = PYTHONPATH=.:.. $(ENV)/bin/python
endif

# Server settings
SERVER_HOST ?= 0.0.0.0
SERVER_PORT ?= 8300

# Test settings
COVERAGE_DIR ?= /tmp/$(APP)-coverage

bootstrap:
	bootstrapper -e $(ENV)/

clean:
	find . -name "*.pyc" -delete
	find . -type d -empty -delete
	find . -name __pycache__ -type d -exec rm -rf {} 2> /dev/null +

distclean: clean
	rm -rf ../build ../dist $(ENV)/

pep8:
	$(PEP8) ../$(APP).py
	$(PEP8) --exclude=$(ENV) $(PROJECT)

server: clean pep8
	$(PYTHON) app.py $(SERVER_HOST):$(SERVER_PORT)

shell:
	$(IPYTHON) --deep-reload --no-banner --no-confirm-exit --pprint

test: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(PROJECT)/ \
	--with-coverage --cover-branches --cover-erase --cover-package=$(APP) \
	--cover-html --cover-html-dir="$(COVERAGE_DIR)"
