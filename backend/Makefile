.PHONY: test run mockserver integration-test lint shared

run:
	@export FLASK_APP=backend.py; poetry run flask run --host=0.0.0.0 --port=5001

mockserver:
	@export FLASK_APP=mock.py; poetry run flask run --host=0.0.0.0 --port=5001

test:
	@export PYTHONPATH=./; poetry run pytest test/unit

integration-test:
	@export PYTHONPATH=./; poetry run pytest test/integration

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports .

shared:
	@poetry remove shared && poetry add ../shared/

build: clean
	@mkdir -p package
	@poetry export --without webserver --without spacy --without dev -f requirements.txt -o package/requirements.txt --without-hashes
	@touch package/lambda_function.py
	@docker build -t translation-lambda --build-arg FUNCTION=translation .

docker-clean:
	@docker stop translation-lambda
	@docker rm -f translation-lambda

make clean:
	@rm -rf package*