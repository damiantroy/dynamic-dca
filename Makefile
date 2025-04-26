install:
	uv sync

validate:
	uv run pre-commit run --all-files

test:
	uv run -m unittest discover tests/

PHONY: install validate test
