all: check lint

.PHONY: check
check: black flake8

.PHONY: lint
lint: mypy pylint 
	

.PHONY: flake8
flake8:
	$(Q)flake8 src/

.PHONY: black
black:
	$(Q)black --check src/


.PHONY: mypy
mypy:
	$(Q)mypy --disallow-untyped-defs --disallow-incomplete-defs src/

.PHONY: pylint
pylint:
	$(Q)pylint src/

.PHONY: blacken
blacken:
	$(Q)black src/ tests/


