setup:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

setup-dev:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt -r requirements-dev.txt

validate:
	pre-commit run --all-files --config .pre-commit-config.yaml

test:
	python -m unittest discover tests/

PHONY: setup setup-dev pre-commit test
