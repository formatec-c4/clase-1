PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
PYTHON_VERSION := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
VENV_PACKAGE := python$(PYTHON_VERSION)-venv

.PHONY: init ensure-venv run check clean

init:
	$(MAKE) ensure-venv
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

ensure-venv:
	@$(PYTHON) -m venv /tmp/vet-firulais-turnos-venv-test >/dev/null 2>&1 || \
		( echo "Instalando $(VENV_PACKAGE)..." && sudo apt-get update && sudo apt-get install -y $(VENV_PACKAGE) )
	@rm -rf /tmp/vet-firulais-turnos-venv-test

run:
	$(PY) app.py

check:
	$(PYTHON) -m py_compile app.py

clean:
	rm -rf $(VENV) __pycache__
