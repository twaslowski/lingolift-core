.PHONY: test run mockserver integration-test lint shared

webserver:
	@export FLASK_APP=webserver.py; poetry run flask run --host=0.0.0.0 --port=5001

test:
	@export PYTHONPATH=./; poetry run pytest test/unit

integration-test:
	@export PYTHONPATH=./; poetry run pytest test/integration

lint:
	@poetry run mypy  --no-namespace-packages --ignore-missing-imports .

shared:
	@poetry remove shared && poetry add ../shared/

build:
	@mkdir -p package_generative
	@cp -r lambda_functions_generative.py generative llm util package_generative
	@cd package_generative && zip -r ../package_generative.zip .
	@./build-deps.sh generative

make clean:
	@rm -rf package*
