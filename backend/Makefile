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

language-detection-package:
	@mkdir -p package_language_detection/python/lib/python3.11/site-packages
	@poetry export --only language-detection -f requirements.txt -o package_language_detection/requirements.txt --without-hashes
	@python3.11 -m pip install -r package_language_detection/requirements.txt --target package_language_detection/python/lib/python3.11/site-packages --platform manylinux2014_x86_64 --only-binary=:all:

spacy-models-package:
	@mkdir -p package_spacy_models/python/lib/python3.11/site-packages
	@poetry export --only nlp -f requirements.txt -o package_spacy_models/requirements.txt --without-hashes
	@python3.11 -m pip install -r package_spacy_models/requirements.txt --target package_spacy_models/python/lib/python3.11/site-packages --platform manylinux2014_x86_64 --only-binary=:all:

generative-deps-package:
	@mkdir -p package_generative_deps/python/lib/python3.11/site-packages
	@poetry export --with generative -f requirements.txt -o package_generative_deps/requirements.txt --without-hashes
	@python3.11 -m pip install -r package_generative_deps/requirements.txt --target package_generative_deps/python/lib/python3.11/site-packages --platform manylinux2014_x86_64 --only-binary=:all:

nlp-deps-package:
	@mkdir -p package_nlp_devs/python/lib/python3.11/site-packages
	@poetry export --with nlp -f requirements.txt -o package_nlp_devs/requirements.txt --without-hashes
	@python3.11 -m pip install -r package_nlp_devs/requirements.txt --target package_nlp_deps/python/lib/python3.11/site-packages --platform manylinux2014_x86_64 --only-binary=:all:

generative-lambda:
	@mkdir -p package_generative
	@cp -r lambda_functions_generative.py generative llm util package_generative

nlp-lambda:
	@mkdir -p package_nlp
	@cp -r lambda_functions_nlp.py nlp util package_nlp

make clean:
	@rm -rf package*