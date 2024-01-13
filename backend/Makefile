.PHONY: test run mockserver integration-test lint shared

run:
	@poetry run flask run --host=0.0.0.0 --port=5001

mockserver:
	@export FLASK_APP=mock.py
	@poetry run flask run --host=0.0.0.0 --port=5001

test:
	@poetry run pytest test/unit

integration-test:
	@poetry run pytest test/integration

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports .


shared:
	@poetry remove shared && poetry add ../shared/