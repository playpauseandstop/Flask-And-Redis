.PHONY: bootstrap clean distclean killredis manage redis server shell test

# Project and environment settings
ENV ?= env
ENV24 = $(ENV)-2.4
ENV26 = $(ENV)-2.6
PROJECT = .

# Python settings
PYTHON = PYTHONPATH=.. $(ENV)/bin/python
PYTHON24 = PYTHONPATH=.. $(ENV24)/bin/python
PYTHON26 = PYTHONPATH=.. $(ENV26)/bin/python

MANAGE = $(PYTHON) $(PROJECT)/manage.py
MANAGE24 = $(PYTHON) $(PROJECT)/manage.py
MANAGE26 = $(PYTHON) $(PROJECT)/manage.py

# Server settings
HOST ?= 0.0.0.0
PORT ?= 4353

# Test settings
TEST_ARGS ?= -vf

bootstrap:
	bootstrapper

clean:
	find . -name '*.pyc' -delete

distclean: clean
	rm -rf ../build ../dist $(ENV) $(ENV24)

killredis:
	-kill `ps -o "pid,command" | grep "redis-server redis/backup.conf" | grep -v grep | awk '{print $$1}'`
	-kill `ps -o "pid,command" | grep "redis-server redis/slave.conf" | grep -v grep | awk '{print $$1}'`

manage:
	$(MANAGE) $(COMMAND)

redis:
	[ ! -d redis/backup/ ] && mkdir redis/backup/ || :
	redis-server redis/backup.conf > redis/backup.log &

	[ ! -d redis/slave/ ] && mkdir redis/slave/ || :
	redis-server redis/slave.conf > redis/slave.log &

server:
	$(MANAGE) runserver -t $(HOST) -p $(PORT)

shell:
	$(MANAGE) shell

test:
	PYTHONPATH=.:.. $(ENV)/bin/unit2 discover $(TEST_ARGS) $(PROJECT)/
	PYTHONPATH=.:.. $(ENV24)/bin/unit2 discover $(TEST_ARGS) $(PROJECT)/
	PYTHONPATH=.:.. $(ENV26)/bin/unit2 discover $(TEST_ARGS) $(PROJECT)/
