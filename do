#!/usr/bin/env bash

## test: Runs unit tests
function task_test {
  poetry run coverage run -m pytest
}

function task_coverage() {
  task_test
  poetry run coverage html
  poetry run coverage xml -o test/coverage.xml
  poetry run coverage-badge -f -o test/coverage.svg
}

function task_pc() {
  poetry run pre-commit run --all-files
}

function task_export_requirements() {
  # Export requirements to package/requirements.txt
  # Any additional input arguments are passed to poetry export, such as `--with dev`.
  mkdir package
  poetry export -f requirements.txt -o package/requirements.txt --without-hashes "$@"
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
