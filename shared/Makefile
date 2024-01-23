.PHONY: test

test:
	@poetry run pytest shared/ --ignore shared/test_client.py

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports shared/
