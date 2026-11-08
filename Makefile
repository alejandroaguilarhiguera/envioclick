
PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt

dev:
	.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 9000