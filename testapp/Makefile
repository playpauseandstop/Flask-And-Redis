# Project and environment settings
env = env
project = .
python = PYTHONPATH=.. $(env)/bin/python

# Server settings
IP ?= 0.0.0.0
PORT ?= 4353

server:
	$(python) $(project)/app.py $(IP):$(PORT)

test:
	$(python) $(project)/tests.py
