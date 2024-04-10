SHELL := /bin/bash
PHONY :=

VENV := .venv
DOCK_CLI := dock_cli
EGG_INFO := dock_cli.egg-info
DIST_DIR := dist

GIT ?= git
PYTHON ?= python3
VENV_PIP ?= $(VENV)/bin/pip3
VENV_PYTHON ?= $(VENV)/bin/python3
VENV_PYLINT ?= $(VENV)/bin/pylint
VENV_PYTEST ?= $(VENV)/bin/pytest
VENV_DOCK ?= $(VENV)/bin/dock

$(VENV):
	@set -euo pipefail; \
	$(PYTHON) -m venv $(VENV); \
	$(VENV_PIP) install -Uq pip setuptools wheel; \
	$(VENV_PIP) install -Uqe .; \
	echo -e "Successfully created a new virtualenv $(VENV) in $$PWD";

PHONY += check-python-version
check-python-version:
	@set -euo pipefail; \
	python_version=$$($(PYTHON) --version 2>&1 | awk '{print $$2}'); \
	major_version=$$(echo $$python_version | cut -d. -f1); \
	minor_version=$$(echo $$python_version | cut -d. -f2); \
	if [ $$major_version -lt 3 ] || { [ $$major_version -eq 3 ] && [ $$minor_version -lt 7 ]; }; then \
		echo "Require Python 3.7 or higher." ; \
		exit 1; \
	fi;

PHONY += init
init: check-python-version $(VENV)

PHONY += list
list: init
	@set -euo pipefail; \
	$(VENV_PIP) list;

PHONY += test
test: init .pylintrc test/requirements.txt
	@set -euo pipefail; \
	$(VENV_PIP) install -Uqr test/requirements.txt; \
	$(VENV_PIP) list; \
	$(VENV_PYLINT) $(DOCK_CLI) --rcfile .pylintrc --reports y; \
	$(VENV_PYTEST) test;

PHONY += clean
clean:
	@rm -rf $(VENV) $(EGG_INFO) $(DIST_DIR)

PHONY += create-tag
create-tag: init
	@set -euo pipefail; \
	dock_version=$$($(VENV_DOCK) --version | cut -d' ' -f3); \
	$(GIT) tag $$dock_version;

PHONY += push-tag
push-tag: init
	@set -euo pipefail; \
	dock_version=$$($(VENV_DOCK) --version | cut -d' ' -f3); \
	$(GIT) push origin $$dock_version;

PHONY += build-package
build-package: init
	@set -euo pipefail; \
	$(VENV_PIP) install -Uq build; \
	$(VENV_PYTHON) -m build --outdir $(DIST_DIR);

PHONY += upload-package
upload-package: init
	@set -euo pipefail; \
	$(VENV_PIP) install -Uq twine; \
	$(VENV_PYTHON) -m twine check --strict $(DIST_DIR)/*; \
	$(VENV_PYTHON) -m twine upload $(DIST_DIR)/*;

.PHONY: $(PHONY)
