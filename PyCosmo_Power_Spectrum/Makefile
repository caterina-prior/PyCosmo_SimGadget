# === Configuration ===
VENV := ./venv_pycosmo
# Parameter file configuration
PARAM_FILE := pycosmo_input_32.param
# Cache directory for sympy2c
CACHE_DIR := $(HOME)/_cache/sympy2c
# Get the absolute path of the repository root
ROOT_DIR := $(shell pwd)


# === Platform Detection ===

UNAME_S := $(shell uname -s)
UNAME_R := $(shell uname -r)

ifeq ($(UNAME_S),Linux)
	ifneq (,$(findstring Microsoft,$(UNAME_R)))
		PLATFORM := wsl
	else
		PLATFORM := linux
	endif
endif

ifeq ($(UNAME_S),Darwin)
	PLATFORM := mac
endif

# === Targets ===

.PHONY: all venv setup install install_deps clear_cache test test_full run clean help

all: setup

# Create a virtual environment with Python 3.9
venv:
	@echo "Setting up virtual environment in $(VENV)..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found at $(VENV)! Please create it with Python 3.9 first."; \
		exit 1; \
	fi
	@echo "Ensuring pip is installed in the virtual environment..."
	$(VENV)/bin/python -m ensurepip

# Install Python dependencies
install: venv
	@echo "Installing Python dependencies from requirements.txt..."
	@$(VENV)/bin/pip3 install -r requirements.txt

# Install system and Python build dependencies
install_deps: venv
	@echo "Installing/upgrading build tools and system deps..."
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel

	@if command -v apt-get >/dev/null; then \
		if command -v sudo >/dev/null; then \
			echo "Detected apt-based system. Installing GSL..."; \
			sudo apt-get update; \
			sudo apt-get install -y build-essential libgsl-dev autoconf automake libtool; \
			sudo apt-get install -y texlive-latex-base texlive-fonts-recommended dvipng cm-super; \
		else \
			echo "Skipping apt-get installation: sudo not found."; \
		fi; \
	elif command -v brew >/dev/null; then \
		echo "Detected macOS with Homebrew. Installing GSL..."; \
		brew install gsl; \
	else \
		echo "No known package manager found. Please install GSL manually."; \
	fi


# One-time full setup (venv + pip + system deps)
setup: venv install install_deps
	@echo "Environment setup complete."
	@echo "Reminder: Source 'setup_pycosmo.sh' before running."

# Run tests (no rebuilds or cache clearing)
test:
	@echo "Running tests..."
	@set -e; \
	PYTHON_SYMPY2C_USE_SHARED_GSL=1 $(VENV)/bin/python -m pytest tests/ || echo "Tests failed"

# Optional: force rebuild GSL wrapper + clear cache before testing
test_full: install_deps clear_cache
	@echo "Running full test suite (with GSL rebuild)..."
	@set -e; \
	PYTHON_SYMPY2C_USE_SHARED_GSL=1 $(VENV)/bin/python -m pytest tests/

# Run the main script with a specified parameter file
run:
	@echo "Usage: make run PARAM=your_param_file.param"
	@if [ -z "$(PARAM)" ]; then \
		echo "Error: No parameter file specified. Use PARAM=your_param_file.param"; \
		exit 1; \
	fi
	@echo "Running custom power spectrum generator with $(PARAM)..."
	$(VENV)/bin/python -m power_spectrum_generation.custom_power_spectrum $(PARAM)

phase_space:
ifndef PARTICLES
	$(error You must specify PARTICLES, e.g. make phase_space PARTICLES=128)
endif
	@echo "Generating phase space plots for $(PARTICLES) particles..."
	$(VENV)/bin/python plotting/phase_space_diagrams.py $(PARTICLES)

# Clear the sympy2c cache
clear_cache:
	@echo "Clearing sympy2c cache at $(CACHE_DIR)..."
	rm -rf $(CACHE_DIR)

# Clean up virtual environment and bytecode
clean:
	@echo "Cleaning up virtual environment and Python artifacts..."
	rm -rf build
	rm -f *.o
	rm -rf $(VENV) __pycache__
	find . -name "*.pyc" -delete

# Help message
help:
	@echo "Usage:"
	@echo "  source setup_pycosmo.sh      # set up env for PyCosmo"
	@echo "  make run PARAM=...           # run PyCosmo + N-GenIC"
	@echo "  make clean                   # remove venv and artifacts"
