#!/bin/bash

ACTION=$1
FUNCTION=$2

if [ -z "$ACTION" ]; then
  echo "Missing action."
  exit 1
fi

function _post() {
    rm -rf package
    rm -f Dockerfile
}

function _package() {
  mkdir -p package
  poetry export --without webserver --without spacy --without dev -f requirements.txt -o package/requirements.txt --without-hashes
}

function _build() {
  FUNCTION=$1
  sed "s/\$FUNCTION/$FUNCTION/g" Dockerfile.template > Dockerfile

  docker build -t "$FUNCTION"-lambda .
}

function _run() {
  FUNCTION=$1
  docker run -p 9000:8080 "$FUNCTION"-lambda:latest --name "$FUNCTION"-lambda
}

function _clean() {
  docker rm -f "$FUNCTION"-lambda
}

# perform action with function
_$ACTION $FUNCTION