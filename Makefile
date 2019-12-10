# This Makefile requires the following commands to be available:
# * python3.6

DEPS=requirements.txt

PIP="venv/bin/pip"
TOX="venv/bin/tox"
PYTHON="venv/bin/python"
TOX_PY_LIST="$(shell $(TOX) -l | grep ^py | xargs | sed -e 's/ /,/g')"

.PHONY: clean pyclean test lint isort format docker

tox: venv
	$(TOX)

pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build
	@rm -rf coverage.xml .coverage

clean: pyclean
	@rm -rf venv

check_dependency_tree: venv
	@$(PIP) check

venv:
	@python3.6 -m venv venv
	@$(PIP) install -U "pip>=7.0" -q
	@$(PIP) install -r $(DEPS)
	@$(PIP) install -e .

test: clean tox check_dependency_tree

test/%: venv pyclean
	$(TOX) -e $(TOX_PY_LIST) -- $*

lint: venv
	@$(TOX) -e lint,isort-check,black-check

isort: venv
	@$(TOX) -e isort-fix

format: venv
	@$(TOX) -e isort-fix,black-fix

build: clean venv tox

changelog: venv
	venv/bin/gitchangelog
