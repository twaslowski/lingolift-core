.PHONY: test run mockserver

run:
	@poetry run flask run --host=0.0.0.0 --port=5001

mockserver:
	@export FLASK_APP=mock.py
	@poetry run flask run --host=0.0.0.0 --port=5001

test:
	@poetry run pytest test/unit

integration-test:
	@poetry run pytest test/integration