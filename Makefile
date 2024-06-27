SHELL := /bin/bash

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
	$(VENV_PIP) install -Uqe .[test]; \
	$(VENV_PIP) list; \
	echo -e "Successfully created a new virtualenv $(VENV) in $$PWD";

.DEFAULT_GOAL: init
.PHONY: init
init: $(VENV)

.PHONY: test
test: init
	@set -euo pipefail; \
	$(VENV_PYLINT) $(DOCK_CLI); \
	$(VENV_PYTEST);

.PHONY: clean
clean:
	@rm -rf $(VENV) $(EGG_INFO) $(DIST_DIR)

.PHONY: create-tag
create-tag: init
	@set -euo pipefail; \
	dock_version=$$($(VENV_DOCK) --version); \
	$(GIT) tag $$dock_version;

.PHONY: push-tag
push-tag: init
	@set -euo pipefail; \
	dock_version=$$($(VENV_DOCK) --version); \
	$(GIT) push origin $$dock_version;

.PHONY: build-package
build-package: init
	@set -euo pipefail; \
	$(VENV_PIP) install -Uq build; \
	$(VENV_PYTHON) -m build --outdir $(DIST_DIR);

.PHONY: upload-package
upload-package: init
	@set -euo pipefail; \
	$(VENV_PIP) install -Uq twine; \
	$(VENV_PYTHON) -m twine check --strict $(DIST_DIR)/*; \
	$(VENV_PYTHON) -m twine upload $(DIST_DIR)/*;
