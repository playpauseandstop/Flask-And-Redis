.PHONY: bootstrap clean distclean server shell test

# Project and environment settings
env = env
env24 = $(env)-2.4
project = .
python = PYTHONPATH=.. $(env)/bin/python
python24 = PYTHONPATH=.. $(env24)/bin/python

# Server settings
IP ?= 0.0.0.0
PORT ?= 4353

bootstrap:
	bootstrap.py --copy-virtualenv

clean:
	find . -name '*.pyc' -delete

distclean: clean
	rm -rf build dist $(env) $(env24)

server:
	$(python) $(project)/app.py $(IP):$(PORT)

shell:
	PYTHONPATH=.:.. $(env)/bin/ipython --color-info --no-banner --pprint

test:
	$(python) $(project)/tests.py
	$(python24) $(project)/tests.py
