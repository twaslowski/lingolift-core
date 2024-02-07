.PHONY: test

test:
	@poetry run pytest shared/ --ignore shared/test/smoke_test.py

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports shared/

smoketest:
	@poetry run pytest shared/smoke_test.py