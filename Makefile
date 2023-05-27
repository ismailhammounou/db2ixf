SHELL = /bin/bash
PROJECT_ROOT = $(shell pwd)
VENV_NAME = venv
VENV_DIR = $(PROJECT_ROOT)/$(VENV_NAME)
VENV_BIN = $(VENV_DIR)/bin
VENV_LIBRARY_BIN = $(VENV_DIR)/Library/bin

# Python
PYTHON_VERSION = 3.9.16

# Project Directories
ANACONDA_DIR = $(PROJECT_ROOT)/contributing/anaconda
DEV_DEPENDENCIES_DIR = $(PROJECT_ROOT)/dependencies/dev
DEPENDENCIES_DIR = $(PROJECT_ROOT)/dependencies/release

PYTEST_OUTPUT_DIR = $(REPORT_OUTPUT_DIR)/test
REPORT_OUTPUT_DIR = $(PROJECT_ROOT)/report
COVERAGE_OUTPUT_DIR = $(REPORT_OUTPUT_DIR)/coverage
FLAKE8_OUTPUT_DIR = $(REPORT_OUTPUT_DIR)/flake8
SECURITY_OUTPUT_DIR = $(REPORT_OUTPUT_DIR)/security

DOCS_OUTPUT_DIR = $(PROJECT_ROOT)/site
SDIST_OUTPUT_DIR = $(PROJECT_ROOT)/dist

PYTEST_TARGET_DIR = $(PROJECT_ROOT)/target/pytest
LUIGI_TARGET_DIR = $(PROJECT_ROOT)/target/luigi

# windows / unix support
ifeq ($(OS),Windows_NT)
	VENV_BIN = $(PROJECT_ROOT)/venv/Scripts
endif

# Export some environment variables
export PYTHONPATH := $(PROJECT_ROOT)/src/:$(PROJECT_ROOT)
export PATH := $(HADOOP_HOME)/bin:$(VENV_DIR):$(VENV_BIN):$(VENV_LIBRARY_BIN):$(PATH)
export CONDARC = $(ANACONDA_DIR)/.condarc
export PACKAGE_NAME = $(shell python setup.py --name 2> /dev/null)
export FULL_PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null)
export PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null | grep -Po '^\d.\d.\d')
export SHORT_PACKAGE_VERSION = $(shell python setup.py --version 2> /dev/null | grep -Po '^\d.\d')

# Activate virtual environment
VENV_ACTIVATE = source activate $(PROJECT_ROOT)/$(VENV_NAME)
# Remote doc
REMOTE_DOC_ROOT = $(DOC_REPO_ROOT)/$(PACKAGE_NAME)



# ============================
#   INFO
# ============================
all: info

.PHONY: show-vars
show-vars: ## Show environment variables
	@echo "----------------------------------------------------------------------------------------"
	@echo "PACKAGE_NAME : $(PACKAGE_NAME)"
	@echo "PACKAGE_VERSION : $(FULL_PACKAGE_VERSION)"
	@echo "----------------------------------------------------------------------------------------"
	@echo " Environment variables "
	@echo "----------------------------------------------------------------------------------------"
	@echo "PROJECT_ROOT : $(PROJECT_ROOT)"
	@echo "PYTHONPATH : $(PYTHONPATH)"
	@echo "PATH : $(PATH)"

.PHONY: name
name: ## Show package name
	@echo "$(PACKAGE_NAME)"

.PHONY: version
version: ## Show package version
	@echo "$(FULL_PACKAGE_VERSION)"

.PHONY: info
info: ## Show this information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



# ============================
#   ENV
# ============================
$(VENV_DIR):
	conda create --verbose --prefix $(VENV_DIR) python=$(PYTHON_VERSION) --no-default-packages --yes
	cp -f $(ANACONDA_DIR)/.condarc $(VENV_DIR)/.condarc ||
	cp -f $(ANACONDA_DIR)/pip.conf $(VENV_DIR)/pip.conf || true
	cp -f $(ANACONDA_DIR)/pip.conf $(VENV_DIR)/pip.ini || true
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
clean: clean-reports clean-docs clean-pyc clean-dist clean-luigi  ## Clean artifacts
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean-reports
clean-reports:  ## Clean reports
	rm -rf $(REPORT_OUTPUT_DIR) || true

.PHONY: clean-docs
clean-docs: ## Clean documentation directory.
	rm -rf $(DOCS_OUTPUT_DIR) || true

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
clean-dist: ## Clean dist
	rm -rf $(SDIST_OUTPUT_DIR) || true
	rm -rf build || true

.PHONY: clean-security
clean-security:  ## Clean security reports
	rm -rf $(SECURITY_OUTPUT_DIR) || true

.PHONY: clean-pytest
clean-pytest:  ## Clean pytest reports
	rm -rf $(PYTEST_OUTPUT_DIR) || true
	rm -rf $(PYTEST_TARGET_DIR) || true
	rm -rf $(COVERAGE_OUTPUT_DIR) || true

.PHONY: clean-flake8
clean-flake8:  ## Clean flake8 reports
	rm -rf $(FLAKE8_OUTPUT_DIR) || true

.PHONY: clean-changelog
clean-changelog: ## Clean changelog fragments (records).
	rm -rf resources/changelog/*.md || true

.PHONY: clean-ghp
clean-ghp: ## Clean documentation branches.
	git branch -d github-pages
	git branch -d gh-pages

.PHONY: clean-luigi
clean-luigi:  ## Clean deployment package and temporary files.
	rm -rf $(LUIGI_TARGET_DIR)/dist || true
	rm -rf $(LUIGI_TARGET_DIR)/workflow.tar.gz || true



# ============================
#   CHANGELOG
# ============================
.PHONY: record-add
record-add: ## Record a new change by creating news fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).added.md

.PHONY: record-change
record-change: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).changed.md

.PHONY: record-deprecate
record-deprecate: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).deprecated.md

.PHONY: record-remove
record-remove: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).removed.md

.PHONY: record-fix
record-fix: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).fixed.md

.PHONY: record-secure
record-secure: ## Record a new change by creating new fragments (Read changelog.md).
	echo "Message: $(msg)"
	echo "Issue: AZFRICSD-$(nbr)"
	$(VENV_ACTIVATE); towncrier create -c "$(msg)" $(nbr).security.md

.PHONY: changelog
changelog: ## Update CHANGELOG.md with the last news fragments.
	$(VENV_ACTIVATE); towncrier build --yes --version $(PACKAGE_VERSION) 2> /dev/null || true
	rm -rf docs/markdown/changelog.md || true
	cp -rf CHANGELOG.md docs/markdown/changelog.md



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

.PHONY: deploy-docs
deploy-docs: update changelog clean-docs build-docs ## Deploy documentation to nexus.
	echo "Deploying the documentation to nexus"
	$(VENV_ACTIVATE); azfr-document-deploy \
		-i $(DOCS_OUTPUT_DIR) \
		-n `python setup.py --name` \
		-c $(DOC_REPO_CERT) \
		-o $(DOC_REPO_ROOT) \
		-u $(DOC_REPO_USER) \
		-p $(DOC_REPO_PASS)

.PHONY: mkdocs-deploy-docs
mkdocs-deploy-docs: update changelog clean-docs build-docs  ## Deploy documentation to github pages (gh-pages) using Mkdocs.
	echo "Deploying the documentation to github pages (gh-pages) using Mkdocs"
	$(VENV_ACTIVATE); mkdocs gh-deploy --clean \
		--message "Deploy documentation ({sha}) for the version `$(PACKAGE_VERSION)`" \
		--config-file mkdocs.yml \
		--verbose \
		--force



# ============================
#   TEST
# ============================
.PHONY: check-code
check-code: clean-flake8 ## Check code with static analysis.
	mkdir -p $(FLAKE8_OUTPUT_DIR)
	$(VENV_ACTIVATE); flake8 --radon-max-cc=10 --format=codeclimate --output-file=$(FLAKE8_OUTPUT_DIR)/codeclimate.json ./src/ || true
	$(VENV_ACTIVATE); flake8 --radon-max-cc=10 --output-file=$(FLAKE8_OUTPUT_DIR)/quality.txt ./src/ || true
	$(VENV_ACTIVATE); flake8 --radon-max-cc=10 --format=html --htmldir=$(FLAKE8_OUTPUT_DIR)/html  ./src/ || true

.PHONY: test
test: update check-code ## Launch tests with coverage.
	$(VENV_ACTIVATE); pytest -vv -rA --durations 0 --continue-on-collection-errors \
	--numprocesses logical --maxprocesses 1 --dist loadfile \
	--asyncio-mode strict \
	--cov

.PHONY: test-with-report
test-with-report: update check-code clean-pytest ## Test with reports.
	mkdir -p $(PYTEST_TARGET_DIR)
	mkdir -p $(COVERAGE_OUTPUT_DIR)/html
	$(VENV_ACTIVATE); pytest -vv -rA --basetemp $(PYTEST_TARGET_DIR) \
	--durations=0 --continue-on-collection-errors \
	--numprocesses logical --maxprocesses 1 --dist loadfile \
	--asyncio-mode strict \
	--html=$(PYTEST_OUTPUT_DIR)/pytests.html --self-contained-html \
	--junitxml=$(PYTEST_OUTPUT_DIR)/junit.xml \
	--cov \
	&& coverage json  --pretty-print --ignore-errors -o $(COVERAGE_OUTPUT_DIR)/coverage.json \
	&& coverage xml --ignore-errors -o $(COVERAGE_OUTPUT_DIR)/coverage.xml \
	&& coverage html -d $(COVERAGE_OUTPUT_DIR)/html



# ============================
#   SAFETY
# ============================
.PHONY: safety-check
safety-check: clean-security update ## Check dependencies vulnerabilities using pyup.io safety package.
	@echo "----------------------------------------------------------------------------------------"
	@echo "------------------------          VULNERABILITY CHECK         --------------------------"
	@echo "----------------------------------------------------------------------------------------"
	mkdir -p $(SECURITY_OUTPUT_DIR)
	$(VENV_ACTIVATE); safety check --full-report --output=text -i 51457  > $(SECURITY_OUTPUT_DIR)/safety-report.txt
	$(VENV_ACTIVATE); safety check --output=json -i 51457 --save-json=$(SECURITY_OUTPUT_DIR)

.PHONY: safety-review
safety-review: safety-check ## Review a pyup.io safety report.
	$(VENV_ACTIVATE); safety review --full-report --file=$(SECURITY_OUTPUT_DIR)/safety-report.json



# ============================
#   Package
# ============================
.PHONY: build-package
build-package: clean-pyc clean-dist ## Build the python package.
	$(VENV_ACTIVATE); python -m pip install --upgrade build -c $(DEV_DEPENDENCIES_DIR)/constraints.txt
	$(VENV_ACTIVATE); python -m build --no-isolation

.PHONY: deploy-package
deploy-package: build-package ## Deploy the python package
	$(VENV_ACTIVATE); python -m pip install --upgrade twine -c $(DEV_DEPENDENCIES_DIR)/constraints.txt
	echo "deploy :twine upload --repository-url $(PYPI_REPO_URL) --username $(PYPI_REPO_USER)"
	$(VENV_ACTIVATE); python -m twine upload --verbose --non-interactive \
	--repository-url $(PYPI_REPO_URL) \
	--username $(PYPI_REPO_USER) \
	--password $(PYPI_REPO_PASS) \
	dist/*
