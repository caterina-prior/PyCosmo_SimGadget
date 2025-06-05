# === Configuration ===


VENV := venv # Define the virtual environment directory
PARAM_FILE := pycosmo_input_32.param # Parameter file configuration
CACHE_DIR := $(HOME)/_cache/sympy2c # Cache directory for sympy2c
ROOT_DIR := $(shell pwd) # Get the absolute path of the repository root


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

# === GSL Configuration ===


ifeq ($(PLATFORM),mac)
	GSL_LIB_PATH := /usr/local/lib
	GSL_INCLUDE_PATH := /usr/local/include
else
	GSL_LIB_PATH := /usr/lib/x86_64-linux-gnu
	GSL_INCLUDE_PATH := /usr/include
endif


# === Compiler Flags ===

CFLAGS += -I$(GSL_INCLUDE_PATH)
LDFLAGS += -L$(GSL_LIB_PATH) -lgsl -lgslcblas


# === Environment Variables ===


export CFLAGS
export LDFLAGS
export PYTHONPATH := $(ROOT_DIR)
export CC := gcc
export CXX := g++
export SYMPY2C_USE_SYSTEM_GSL := 1
export LD_LIBRARY_PATH := $(GSL_LIB_PATH):$(LD_LIBRARY_PATH)


# === Targets ===


.PHONY: all venv setup install install_deps clear_cache test test_full run clean

all: setup run

# Create a virtual environment with Python 3.9
venv:
	@echo "Setting up virtual environment with Python 3.9..."
	@if ! command -v python3.9 >/dev/null; then \
		echo "python3.9 not found! Please install it."; \
		exit 1; \
	fi
	@if [ ! -d "$(VENV)" ]; then \
		python3.9 -m venv $(VENV); \
	fi

# Install Python dependencies
install: venv
	@echo "Installing Python dependencies from requirements.txt..."
	$(VENV)/bin/pip install -r requirements.txt

# Install system and Python build dependencies
install_deps: venv
	@echo "Installing/upgrading build tools and system deps..."
	$(VENV)/bin/pip install --upgrade pip setuptools wheel

	@if command -v apt-get >/dev/null; then \
		echo "Detected apt-based system. Installing GSL..."; \
		sudo apt-get update; \
		sudo apt-get install -y build-essential libgsl-dev autoconf automake libtool; \
		sudo apt-get install -y texlive-latex-base texlive-fonts-recommended dvipng cm-super; \
	elif command -v brew >/dev/null; then \
		echo "Detected macOS with Homebrew. Installing GSL..."; \
		brew install gsl; \
	else \
		echo "No known package manager found. Please install GSL manually."; \
	fi
	
# One-time full setup (venv + pip + system deps)
setup: venv install install_deps
	@echo "Environment setup complete."
	@echo "Reminder: If you encounter shared library issues, run:"
	@echo "  export LD_LIBRARY_PATH=$(GSL_LIB_PATH):\$$LD_LIBRARY_PATH"

# Clear the sympy2c cache
clear_cache:
	@echo "Clearing sympy2c cache at $(CACHE_DIR)..."
	rm -rf $(CACHE_DIR)

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

# Create power spectrum plots
# Save .pngs in folder

# Compare PyCosmo-generated initial conditions with automatic ngenic ones
# Also generate phase-space diagrams, saved in folder 

# Run the main script with a specified parameter file
run:
	@echo "Usage: make run PARAM=your_param_file.param"
	@if [ -z "$(PARAM)" ]; then \
		echo "Error: No parameter file specified. Use PARAM=your_param_file.param"; \
		exit 1; \
	fi
	@echo "Running custom power spectrum generator with $(PARAM)..."
	$(VENV)/bin/python -m power_spectrum_generation.custom_power_spectrum $(PARAM)

	@echo "Running N-GenIC with $(PARAM)..."
	@cd .. && ../ngenic/N-GenIC $(lastword $(PARAM))


# Clean up virtual environment and bytecode
clean:
	@echo "Cleaning up virtual environment and Python artifacts..."
	rm -rf build
	rm -f *.o
	rm -rf $(VENV) __pycache__
	find . -name "*.pyc" -delete
