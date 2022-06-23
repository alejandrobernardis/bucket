#!/usr/bin/env make
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2021-04-20

SRC_PATH:=${CURDIR}/src
VENV_PATH:=${CURDIR}/.venv

.PHONY: wheel
wheel:
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: clean-egg-info
clean-egg-info:
	-find ${CURDIR} \( -name *.egg-info -a -type d -not -path '$(VENV_PATH)/*' \) -exec rm -rf {} + 2> /dev/null

.PHONY: clean-python-cache
clean-python-cache:
	-find ${CURDIR} \( -name __pycache__ -o -type d -empty \) -exec rm -rf {} + 2> /dev/null

.PHONY: clean-general
clean-general:
	-rm -f `find $(SRC_PATH) -type f -name '*~'`
	-rm -f `find $(SRC_PATH) -type f -name '.*~'`
	-rm -f `find $(SRC_PATH) -type f -name '@*'`
	-rm -fr ${PWD}/build ${PWD}/dist

.PHONY: clean-data
clean-data:
	-sudo rm -fr ${CURDIR}/.data

.PHONY: clean
clean: clean-egg-info clean-python-cache clean-general clean-data

.PHONY: req
req:
	 poetry export --no-interaction --no-ansi --format requirements.txt --output $(CURDIR)/requirements.txt
