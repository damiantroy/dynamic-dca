pre-commit:
	pre-commit run --all-files

test:
	python -m unittest discover tests/

PHONY: test pre-commit
