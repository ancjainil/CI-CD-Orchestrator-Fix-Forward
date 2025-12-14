PYTHON := python
PIP := pip

install:
	cd backend && $(PIP) install -r requirements.txt

dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

worker:
	cd backend && celery -A app.tasks worker --loglevel=info

lint:
	cd backend && $(PYTHON) -m compileall app

test:
	cd backend && pytest -q
