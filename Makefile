SHELL = /bin/bash
PROJECT_ROOT = $(shell pwd)
VENV_NAME = venv
VENV_DIR = $(PROJECT_ROOT)/$(VENV_NAME)
VENV_BIN = $(VENV_DIR)/bin
VENV_LIBRARY_BIN = $(VENV_DIR)/Library/bin

# Windows support
ifeq ($(OS),Windows_NT)
	VENV_BIN = $(PROJECT_ROOT)/venv/Scripts
endif


# Project Directories
DEV_DEPENDENCIES_DIR = $(PROJECT_ROOT)/dependencies/dev
DEPENDENCIES_DIR = $(PROJECT_ROOT)/dependencies/release

REPORT_TARGET_DIR = $(PROJECT_ROOT)/target/report
PYTEST_REPORT_DIR = $(REPORT_TARGET_DIR)/pytest
COVERAGE_REPORT_DIR = $(REPORT_TARGET_DIR)/coverage
FLAKE8_REPORT_DIR = $(REPORT_TARGET_DIR)/flake8
SECURITY_REPORT_DIR = $(REPORT_TARGET_DIR)/security

TEST_TARGET_DIR = $(PROJECT_ROOT)/target/test

DOCS_SITE_DIR = $(PROJECT_ROOT)/site

SRC_DIST_DIR = $(PROJECT_ROOT)/dist


# Export some environment variables
export PYTHONPATH := $(PROJECT_ROOT)/src/:$(PROJECT_ROOT)
export PACKAGE_NAME = $(shell python setup.py --name 2> /dev/null)
export FULL_PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null)
export PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null | grep -Po '^\d.\d.\d')
export SHORT_PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null | grep -Po '^\d.\d')

# Activate virtual environment
VENV_ACTIVATE = source activate $(PROJECT_ROOT)/$(VENV_NAME)



# ============================
#   INFO
# ============================
all: info

.PHONY: info
info: ## Show this information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



# ============================
#   ENV
# ============================
$(VENV_DIR):
	conda create --verbose --prefix $(VENV_DIR) --no-default-packages --yes
	$(VENV_ACTIVATE); python -m pip install -U -e . -r $(DEV_DEPENDENCIES_DIR)/requirements.txt -c $(DEV_DEPENDENCIES_DIR)/constraints.txt

venv: $(VENV_DIR) ## Create virtualenv

.PHONY: update
update: venv ## Update dependencies
	$(VENV_ACTIVATE); python -m pip install -U -e . -r $(DEV_DEPENDENCIES_DIR)/requirements.txt -c $(DEV_DEPENDENCIES_DIR)/constraints.txt

.PHONY: freeze
freeze: ## List dependencies
	$(VENV_ACTIVATE); pip freeze > requirements.freeze.txt



# ============================
#   CLEAN
# ============================
.PHONY: clean
clean: clean-pyc clean-dist clean-test clean-reports clean-docs  ## Clean artifacts
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## Clean python artifacts
	@find . -name '*.eggs' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -rf {} +
	@find . -name '*.pyo' -exec rm -rf {} +
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '.pytest_cache' -exec rm -rf {} +
	@find . -name '.coverage*' -exec rm -rf {} +
	@find . -name 'spark-warehouse*' -exec rm -rf {} +
	@find . -name 'checkpoints*' -exec rm -rf {} +
	@find ./src -type d -empty -delete
	@find ./tests -type d -empty -delete

.PHONY: clean-dist
clean-dist: ## Clean dist directories
	rm -rf $(SRC_DIST_DIR) || true
	rm -rf build || true

.PHONY: clean-reports
clean-reports:  ## Clean reports
	rm -rf $(REPORT_TARGET_DIR) || true

.PHONY: clean-docs
clean-docs: ## Clean documentation site directory.
	rm -rf $(DOCS_SITE_DIR) || true

.PHONY: clean-test
clean-test:  ## Clean test target directory
	rm -rf $(TEST_TARGET_DIR) || true

.PHONY: clean-security
clean-security:  ## Clean security reports
	rm -rf $(SECURITY_REPORT_DIR) || true

.PHONY: clean-flake8
clean-flake8:  ## Clean flake8 reports
	rm -rf $(FLAKE8_REPORT_DIR) || true

.PHONY: clean-changelog
clean-changelog: ## Clean changelog fragments (records).
	rm -rf resources/changelog/*.md || true

.PHONY: clean-local-ghp
clean-local-ghp: ## Clean local documentation branches.
	git branch --delete gh-pages || true
	git branch --delete github-pages || true

.PHONY: clean-remote-ghp
clean-remote-ghp: ## Clean remote documentation branches.
	git push origin --delete gh-pages || true
	git branch origin --delete github-pages || true



# ============================
#   SAFETY
# ============================
.PHONY: safety-check
safety-check: clean-security ## Check dependencies vulnerabilities using pyup.io safety package.
	@echo "----------------------------------------------------------------------------------------"
	@echo "------------------------          VULNERABILITY CHECK         --------------------------"
	@echo "----------------------------------------------------------------------------------------"
	mkdir -p $(SECURITY_REPORT_DIR)
	$(VENV_ACTIVATE); safety check --full-report --output=text -i 51457  > $(SECURITY_REPORT_DIR)/safety-report.txt
	$(VENV_ACTIVATE); safety check --output=json -i 51457 --save-json=$(SECURITY_REPORT_DIR)

.PHONY: safety-review
safety-review: safety-check ## Review a pyup.io safety report.
	$(VENV_ACTIVATE); safety review --full-report --file=$(SECURITY_REPORT_DIR)/safety-report.json



# ============================
#   TEST
# ============================
.PHONY: check-code
check-code: clean-flake8 ## Check code with some static analysis.
	mkdir -p $(FLAKE8_REPORT_DIR)
	$(VENV_ACTIVATE); flake8 --output-file=$(FLAKE8_REPORT_DIR)/codeclimate.json ./src/ || true
	$(VENV_ACTIVATE); flake8 --output-file=$(FLAKE8_REPORT_DIR)/quality.txt ./src/ || true
	$(VENV_ACTIVATE); flake8 --format=html --htmldir=$(FLAKE8_REPORT_DIR)/html  ./src/ || true

.PHONY: test
test: clean-test check-code ## Launch tests with coverage.
	$(VENV_ACTIVATE); pytest -vv -rA \
	--continue-on-collection-errors \
	--numprocesses logical --maxprocesses 1 --dist loadfile \
	--asyncio-mode strict \
	--cov

.PHONY: test-with-report
test-with-report: clean-test check-code ## Launch tests with coverage reports.
	mkdir -p $(TEST_TARGET_DIR)
	mkdir -p $(COVERAGE_REPORT_DIR)/html
	$(VENV_ACTIVATE); pytest -vv -rA --basetemp $(TEST_TARGET_DIR) \
	--continue-on-collection-errors \
	--numprocesses logical --maxprocesses 1 --dist loadfile \
	--asyncio-mode strict \
	--html=$(PYTEST_REPORT_DIR)/pytests.html --self-contained-html \
	--junitxml=$(PYTEST_REPORT_DIR)/junit.xml \
	--cov \
	&& coverage json  --pretty-print --ignore-errors -o $(COVERAGE_REPORT_DIR)/coverage.json \
	&& coverage xml --ignore-errors -o $(COVERAGE_REPORT_DIR)/coverage.xml \
	&& coverage html -d $(COVERAGE_REPORT_DIR)/html



# ============================
#   Package
# ============================
.PHONY: build-package
build-package: clean-pyc clean-dist ## Build the python package.
	$(VENV_ACTIVATE); python -m pip install --upgrade build -c $(DEV_DEPENDENCIES_DIR)/constraints.txt
	$(VENV_ACTIVATE); python -m build --no-isolation

.PHONY: deploy-package
deploy-package: ## Deploy the python package
	$(VENV_ACTIVATE); python -m pip install --upgrade twine -c $(DEV_DEPENDENCIES_DIR)/constraints.txt
	echo "Deployment: Twine uploads to PyPI"
	$(VENV_ACTIVATE); python -m twine upload --verbose dist/*



# ============================
#   CHANGELOG
# ============================
.PHONY: record-add
record-add: ## Record a new change by creating news fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).added.md

.PHONY: record-change
record-change: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).changed.md

.PHONY: record-deprecate
record-deprecate: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).deprecated.md

.PHONY: record-remove
record-remove: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).removed.md

.PHONY: record-fix
record-fix: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).fixed.md

.PHONY: record-secure
record-secure: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: db2ixf-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).security.md

.PHONY: changelog
changelog: ## Update CHANGELOG.md with the last news fragments.
	$(VENV_ACTIVATE); towncrier build --yes --version $(PACKAGE_VERSION) 2> /dev/null || true



# ============================
#   DOCS
# ============================
.PHONY: serve-docs
serve-docs: ## Serve documentation in a live loading mode.
	echo "Serve the documentation using Mkdocs"
	$(VENV_ACTIVATE); mkdocs serve

.PHONY: build-docs
build-docs: ## Build documentation.
	echo "Build the documentation using Mkdocs"
	$(VENV_ACTIVATE); mkdocs build

.PHONY: mkdocs-deploy-docs
mkdocs-deploy-docs: clean-docs build-docs  ## Deploy documentation to github pages (gh-pages) using Mkdocs.
	echo "Deploying the documentation to github pages (gh-pages) using Mkdocs"
	$(VENV_ACTIVATE); mkdocs gh-deploy --clean \
		--message "Deploy documentation ({sha})." \
		--config-file mkdocs.yml \
		--verbose \
		--force