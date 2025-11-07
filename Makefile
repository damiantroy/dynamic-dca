.PHONY: install
install:
	uv sync

.PHONY: validate
validate:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv run pytest

# Scripts
.PHONY: update_balance
update_balance:
	uv run src/dynamic_dca/update_balance.py

.PHONY: update_risk
update_risk:
	uv run src/dynamic_dca/update_risk.py

.PHONY: dynamic_dca
dynamic_dca:
	uv run src/dynamic_dca/dynamic_dca.py

.PHONY: dynamic_dca-email
dynamic_dca-email:
	uv run src/dynamic_dca/dynamic_dca.py -e
