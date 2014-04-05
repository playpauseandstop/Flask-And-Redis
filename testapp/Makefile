.PHONY: bootstrap clean distclean killredis listupdates manage pep8 redis server shell test

# Project and environment settings
APP = flask_redis
PROJECT = .

ENV ?= env
VENV = $(shell python -c 'import sys; print(1 if hasattr(sys, "real_prefix") else "");')

ifneq ($(VENV),)
	NOSETESTS = nosetests
	PEP8 = flake8
	PYTHON = PYTHONPATH=.:.. python
else
	NOSETESTS = $(ENV)/bin/nosetests
	PEP8 = $(ENV)/bin/flake8
	PYTHON = PYTHONPATH=.:.. $(ENV)/bin/python
endif

# Server settings
SERVER_HOST ?= 0.0.0.0
PORT ?= 8300

# Test settings
COVERAGE_DIR ?= /tmp/$(APP)-coverage
TEST_ARGS ?=

bootstrap:
	bootstrapper

clean:
	find . -name "*.pyc" -delete

distclean: clean
	rm -rf ../build ../dist $(ENV)

killredis:
	-kill `ps -o "pid,command" | grep "redis-server redis/backup.conf" | grep -v grep | awk '{print $$1}'`
	-kill `ps -o "pid,command" | grep "redis-server 127.0.0.1:6380" | grep -v grep | awk '{print $$1}'`
	-kill `ps -o "pid,command" | grep "redis-server redis/slave.conf" | grep -v grep | awk '{print $$1}'`
	-kill `ps -o "pid,command" | grep "redis-server 127.0.0.1:6381" | grep -v grep | awk '{print $$1}'`

manage:
	$(PYTHON) $(PROJECT)/manage.py $(COMMAND)

pep8:
	$(PEP8) ../$(APP).py
	$(PEP8) --exclude=$(ENV) $(PROJECT)

redis:
	[ ! -d redis/backup/ ] && mkdir redis/backup/ || :
	redis-server redis/backup.conf > redis/backup.log &

	[ ! -d redis/slave/ ] && mkdir redis/slave/ || :
	redis-server redis/slave.conf > redis/slave.log &

server:
	COMMAND="runserver -t $(SERVER_HOST) -p $(PORT)" $(MAKE) manage

shell:
	COMMAND=shell $(MAKE) manage

test: clean pep8
	$(NOSETESTS) --logging-clear-handlers $(TEST_ARGS) -w $(PROJECT)/ \
	--with-coverage --cover-branches --cover-erase --cover-package=$(APP) \
	--cover-html --cover-html-dir="$(COVERAGE_DIR)"
