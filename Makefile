# Makefile for formatting Python code

# Tools
PYINK = pyink
ISORT = isort

# Get list of Python files modified or added in git
# We filter for .py files that are modified (M), added (A), or untracked (??)
# then extract the filename.
DIRTY_PY_FILES = $(shell git status --porcelain | grep -E '^[ MARC]*.py$$' | awk '{print $$NF}')

# Virtual environment name
VENV_DIR = venv-dev
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
PRECOMMIT = $(VENV_DIR)/bin/pre-commit

# Default target
all: format

# Setup development environment
setup: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements-dev.txt
	@echo "Creating virtual environment $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo "Installing development requirements..."
	$(PIP) install -r requirements-dev.txt
	@echo "Installing pre-commit hooks..."
	$(PRECOMMIT) install
	@echo "Setup complete. Activate the virtual environment using: source $(VENV_DIR)/bin/activate"
	@touch $(VENV_DIR)/bin/activate # Mark as created

# Format dirty Python files using tools from venv
format: $(VENV_DIR)/bin/activate
	@echo "Checking for dirty Python files..."
	@if [ -n "$(DIRTY_PY_FILES)" ]; then \
		echo "Running isort on:\n$(DIRTY_PY_FILES)"; \
		$(VENV_DIR)/bin/$(ISORT) $(DIRTY_PY_FILES); \
		echo "\nRunning pyink on:\n$(DIRTY_PY_FILES)"; \
		$(VENV_DIR)/bin/$(PYINK) $(DIRTY_PY_FILES); \
		echo "\nFormatting complete."; \
	else \
		echo "No dirty Python files to format."; \
	fi

# Format all Python files in the project
format-all: $(VENV_DIR)/bin/activate
	@echo "Running isort on all Python files..."
	find . -path ./$(VENV_DIR) -prune -o -name '*.py' -print0 | xargs -0 $(VENV_DIR)/bin/$(ISORT)
	@echo "Running pyink on all Python files..."
	find . -path ./$(VENV_DIR) -prune -o -name '*.py' -print0 | xargs -0 $(VENV_DIR)/bin/$(PYINK)
	@echo "Full formatting complete."

.PHONY: all setup format format-all
