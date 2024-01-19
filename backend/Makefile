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
	@poetry export --only lambda -f requirements.txt -o package/requirements.txt --without-hashes
	@docker build -t lambda-layer-builder .
	@docker run --name lambda-layer-builder-container lambda-layer-builder
	@docker cp lambda-layer-builder-container:/var/task/dependencies.zip package
	@docker rm lambda-layer-builder-container


make clean:
	@rm -rf package*