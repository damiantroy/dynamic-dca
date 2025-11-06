.PHONY: install
install:
	uv sync

.PHONY: validate
validate:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest
