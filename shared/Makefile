.PHONY: test

test:
	@poetry run pytest shared/

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports shared/
