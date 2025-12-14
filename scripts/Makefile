# Makefile for Digital Clock Application
# Cross-platform build automation

.PHONY: help build clean install test run dev setup-windows setup-linux setup-macos

# Default target
help:
  @echo "Digital Clock Application Build System"
  @echo "======================================"
  @echo ""
  @echo "Available targets:"
  @echo "  build           - Build for current platform"
  @echo "  build-windows   - Build Windows executable"
  @echo "  build-linux     - Build Linux executable"  
  @echo "  build-macos     - Build macOS app bundle"
  @echo "  build-all       - Build for all platforms (requires platform tools)"
  @echo ""
  @echo "  clean           - Clean build artifacts"
  @echo "  install         - Install dependencies"
  @echo "  setup           - Setup development environment"
  @echo "  test            - Run application tests"
  @echo "  run             - Run application in development mode"
  @echo "  dev             - Run in development mode with auto-reload"
  @echo ""
  @echo "  package         - Create distribution packages"
  @echo "  release         - Build release versions for all platforms"

# Detect operating system
UNAME_S := $(shell uname -s 2>/dev/null || echo "Windows")
PYTHON := $(shell which python3 2>/dev/null || which python 2>/dev/null || echo "python")

# Platform-specific settings
ifeq ($(UNAME_S),Darwin)
  PLATFORM := macos
  BUILD_SCRIPT := python build-macos.py
endif
ifeq ($(UNAME_S),Linux)
  PLATFORM := linux
  BUILD_SCRIPT := bash build-unix.sh
endif
ifeq ($(UNAME_S),Windows_NT)
  PLATFORM := windows
  BUILD_SCRIPT := powershell -ExecutionPolicy Bypass -File build-win.ps1
endif
ifneq (,$(findstring MINGW,$(UNAME_S)))
  PLATFORM := windows
  BUILD_SCRIPT := powershell -ExecutionPolicy Bypass -File build-win.ps1
endif

# Virtual environment detection
VENV := $(shell find . -name "activate" -type f 2>/dev/null | head -1)
ifneq ($(VENV),)
  VENV_DIR := $(dir $(VENV))
  ifeq ($(PLATFORM),windows)
    PYTHON := $(VENV_DIR)python.exe
  else
    PYTHON := $(VENV_DIR)python
  endif
endif

# Build targets
build:
	@echo "Building for $(PLATFORM)..."
	$(BUILD_SCRIPT)

build-windows:
	@echo "Building Windows executable..."
	powershell -ExecutionPolicy Bypass -File build-win.ps1

build-linux:
	@echo "Building Linux executable..."
	bash build-unix.sh

build-macos:
	@echo "Building macOS app bundle..."
	python build-macos.py

build-all: clean
	@echo "Building for all platforms..."
	python build.py --platform windows --clean
	python build.py --platform linux --clean
	python build.py --platform macos --clean

# Development targets
run:
	@echo "Running Digital Clock in development mode..."
	$(PYTHON) src/main.py

dev: install
	@echo "Starting development server with auto-reload..."
	$(PYTHON) -m watchdog.observers src/ -c "$(PYTHON) src/main.py" --recursive

test:
	@echo "Running tests..."
	$(PYTHON) -m pytest tests/ -v

# Setup and maintenance
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install -r requirements.txt

setup:
	@echo "Setting up development environment for $(PLATFORM)..."
	@$(MAKE) setup-$(PLATFORM)

setup-windows:
	@echo "Setting up Windows development environment..."
	python -m venv .venv
	.venv\\Scripts\\activate && pip install --upgrade pip
	.venv\\Scripts\\activate && pip install -r requirements.txt
	.venv\\Scripts\\activate && pip install pyinstaller

setup-linux:
	@echo "Setting up Linux development environment..."
	python3 -m venv .venv
	.venv/bin/activate && pip install --upgrade pip
	.venv/bin/activate && pip install -r requirements.txt
	.venv/bin/activate && pip install pyinstaller

setup-macos:
	@echo "Setting up macOS development environment..."
	python3 -m venv .venv
	.venv/bin/activate && pip install --upgrade pip
	.venv/bin/activate && pip install -r requirements.txt
	.venv/bin/activate && pip install pyinstaller

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf dist/ build/ *.spec
	@rm -rf __pycache__ src/__pycache__ tests/__pycache__
	@rm -rf .pytest_cache
	@echo "Clean completed."

# Packaging and release
package: build
	@echo "Creating distribution package..."
	@mkdir -p releases/$(PLATFORM)
ifeq ($(PLATFORM),windows)
	@cp dist/DigitalClock.exe releases/$(PLATFORM)/
	@cp -r assets releases/$(PLATFORM)/
	@cd releases/$(PLATFORM) && zip -r ../DigitalClock-$(PLATFORM).zip *
endif
ifeq ($(PLATFORM),linux)
	@cp dist/DigitalClock releases/$(PLATFORM)/
	@cp -r assets releases/$(PLATFORM)/
	@cd releases/$(PLATFORM) && tar -czf ../DigitalClock-$(PLATFORM).tar.gz *
endif
ifeq ($(PLATFORM),macos)
	@cp -r "dist/Digital Clock.app" "releases/$(PLATFORM)/"
	@cd releases/$(PLATFORM) && zip -r ../DigitalClock-$(PLATFORM).zip *
endif
	@echo "Package created in releases/"

release: clean
	@echo "Creating release builds..."
	@mkdir -p releases
	@$(MAKE) package PLATFORM=windows
	@$(MAKE) package PLATFORM=linux
	@$(MAKE) package PLATFORM=macos
	@echo "All release packages created!"

# Info targets
info:
	@echo "Build Environment Information"
	@echo "============================"
	@echo "Platform: $(PLATFORM)"
	@echo "Python: $(PYTHON)"
	@echo "Virtual Env: $(VENV_DIR)"
	@echo "Build Script: $(BUILD_SCRIPT)"

# Check dependencies
check-deps:
	@echo "Checking dependencies..."
	@$(PYTHON) -c "import tkinter; print('✓ tkinter available')" 2>/dev/null || echo "✗ tkinter missing"
	@$(PYTHON) -c "import PIL; print('✓ PIL/Pillow available')" 2>/dev/null || echo "✗ PIL/Pillow missing"
	@$(PYTHON) -c "import dotenv; print('✓ python-dotenv available')" 2>/dev/null || echo "✗ python-dotenv missing"
