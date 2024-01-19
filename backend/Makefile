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
	@poetry export --without dev --without spacy --without webserver -f requirements.txt -o package/requirements.txt --without-hashes
	@poetry run pip install --platform manylinux2014_x86_64 -r package/requirements.txt --target package --only-binary=:all:
	@cp -r llm package && cp -r util package && cp -r service package && cp lambda_function.py package
	@cd package && zip -r ../package.zip . && cd ..


make clean:
	@rm -rf package*