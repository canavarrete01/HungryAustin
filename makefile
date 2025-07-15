.PHONY: setup run_models run_create_db run_main models_html

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python

setup: ## Set up virtual environment and install dependencies
	@echo "Setting up virtual environment and installing dependencies..."
	python -m venv $(VENV_NAME)
	$(VENV_NAME)/bin/pip install -r requirements.txt

run_models:
	@echo "Running models.py..."
	$(PYTHON) models.py

run_create_db:
	@echo "Running Create_db.py..."
	$(PYTHON) Create_db.py

run_main:
	@echo "Running Flask application..."
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENVIRONMENT) $(PYTHON) -m flask run

models_html:
	@echo "Generating HTML documentation for models.py..."
	pydoc3 -w models
	mv models.html templates/ || echo "Make sure the templates/ directory exists."

