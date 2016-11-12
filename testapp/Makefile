.PHONY: bootstrap clean distclean pep8 server shell test wipe

# Project and environment settings
APP = flask_redis
PROJECT = .

ENV ?= env
VENV = $(shell python -c 'import sys; print(int(hasattr(sys, "real_prefix")));')

ifeq ($(VENV),1)
	PYTHON = python
	TOX = tox
else
	PYTHON = $(ENV)/bin/python
	TOX = $(ENV)/bin/tox
endif

# Server settings
SERVER_HOST ?= 0.0.0.0
SERVER_PORT ?= 8300

# Test settings
ifneq ($(TOXENV),)
	tox_args = -e $(TOXENV)
endif

clean:
	find . -name "*.pyc" -delete
	find . -type d -empty -delete
	find . -name __pycache__ -type d -exec rm -rf {} 2> /dev/null +

distclean: clean
	rm -rf ../build ../dist $(ENV)/

install: .install
.install: requirements.txt
	bootstrapper -e $(ENV)/
	touch $@

lint: .install
	TOXENV=flake8 $(MAKE) test

server: .install
	$(PYTHON) app.py $(SERVER_HOST):$(SERVER_PORT)

shell:
	$(PYTHON) -m ipython

test: .install
	$(TOX) $(tox_args) $(TOX_ARGS) -- $(TEST_ARGS)

wipe: .install
	$(PYTHON) wipe.py
