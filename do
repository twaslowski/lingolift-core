#!/usr/bin/env bash

## test: Runs unit tests
function task_test {
  poetry run coverage run -m pytest
}

function task_smoke_test() {
  poetry run pytest test/smoketest.py
}

## coverage: Generates test coverage report
function task_coverage() {
  task_test
  poetry run coverage html
  poetry run coverage xml -o test/coverage.xml
  poetry run coverage-badge -f -o test/coverage.svg
}

## pc: runs pre-commit hook
function task_pc() {
  poetry run pre-commit run --all-files
}

## export_requirements: Exports requirements to package/requirements.txt
function task_export_requirements() {
  # Any additional input arguments are passed to poetry export, such as `--with dev`.
  mkdir package
  poetry export -f requirements.txt -o package/requirements.txt --without-hashes "$@"
}

## deploy: Deploys the application to the specified AWS environment
function task_deploy() {
    ENV=$1

    if [ -z "$ENV" ]; then
      echo "Usage: ./do deploy <env>"
      exit 1
    fi

    if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
      echo "Usage: ./do deploy <env>; env must be dev or prod"
      exit 1
    fi

    echo "Deploying to $ENV"
    pushd terraform > /dev/null || exit 1

    terraform init -backend-config="backend_${ENV}.hcl" -reconfigure
    TF_VAR_environment="${ENV}" TF_VAR_commit_sha=$(git rev-parse --short HEAD) terraform apply -auto-approve
}

## build_core_lambdas: packages and zips non-dockerized lambda functions (translation, literal-translation, response suggestions)
function task_build_core_lambdas() {
    mkdir -p package_core/lingolift
    cp -r lingolift/llm \
      lingolift/generative \
      lingolift/util \
      lingolift/core_lambda_context_container.py \
      lingolift/abstract_context_container.py \
      lingolift/core_lambda_handlers.py \
      package_core/lingolift
    cd package_core && zip -r ../package_core.zip .
}

## build_lambda_dependencies: Creates zip archive for core lambda dependencies that are shared between functions as a layer
function task_build_core_lambda_dependencies() {
  PACKAGE_DIRECTORY="package_core_dependencies"

  mkdir -p "${PACKAGE_DIRECTORY}/python/lib/python3.11/site-packages"
  poetry export -f requirements.txt -o "${PACKAGE_DIRECTORY}/requirements.txt" --without-hashes

  python3.11 -m pip install -r "${PACKAGE_DIRECTORY}/requirements.txt" \
    --target "${PACKAGE_DIRECTORY}/python/lib/python3.11/site-packages" \
    --platform manylinux2014_x86_64 --only-binary=:all:

  cd "${PACKAGE_DIRECTORY}" && zip -r "../${PACKAGE_DIRECTORY}.zip" . && cd ..
}

## clean: Removes all lambda package files
function task_clean() {
  rm -rf package*
}

#-------- All task definitions go above this line --------#

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' |  sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
    if [ -n "${cmd}" ]; then
      echo "'$cmd' could not be resolved - please use one of the above tasks"
      exit 1
    fi
fi
