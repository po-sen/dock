SHELL := /bin/bash
PHONY :=

VENV := .venv
DOCK_CLI := dock-cli
EGG_INFO := $(DOCK_CLI)/dock_cli.egg-info

PYTHON ?= python3

$(VENV):
	@set -euo pipefail; \
	$(PYTHON) -m venv $(VENV); \
	$(VENV)/bin/pip install -Uq pip setuptools wheel; \
	$(VENV)/bin/pip install -Uqe $(DOCK_CLI); \
	echo -e "Successfully created a new virtualenv $(VENV) in $$PWD";

PHONY += check-python-version
check-python-version:
	@set -euo pipefail; \
	python_version=$$($(PYTHON) --version 2>&1 | awk '{print $$2}') ; \
	major_version=$$(echo $$python_version | cut -d. -f1) ; \
	minor_version=$$(echo $$python_version | cut -d. -f2) ; \
	if [ $$major_version -lt 3 ] || { [ $$major_version -eq 3 ] && [ $$minor_version -lt 7 ]; }; then \
		echo "Require Python 3.7 or higher." ; \
		exit 1; \
	fi;

PHONY += init
init: check-python-version $(VENV)

PHONY += list
list: init
	@set -euo pipefail; \
	$(VENV)/bin/pip list;

PHONY += test
test: init test/.pylintrc test/requirements.txt
	@set -euo pipefail; \
	$(VENV)/bin/pip install -Uqr test/requirements.txt; \
	$(VENV)/bin/pip list; \
	$(VENV)/bin/pylint $(DOCK_CLI) --rcfile .pylintrc --reports y;

PHONY += clean
clean:
	@rm -rf $(VENV) $(EGG_INFO)

.PHONY: $(PHONY)
