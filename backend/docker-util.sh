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
  _package
  FUNCTION=$1
  sed "s/\$FUNCTION/$FUNCTION/g" Dockerfile.template > Dockerfile

  docker build -t "$FUNCTION"-lambda --platform linux/x86_64 .
  _post
}

function _build_spacy() {
  mkdir -p package
  poetry export --with spacy -f requirements.txt -o package/requirements.txt --without-hashes

  FUNCTION=syntactical_analysis
  sed "s/\$FUNCTION/$FUNCTION/g" Dockerfile.template > Dockerfile

  docker build -t "$FUNCTION"-lambda --platform linux/x86_64 .
  _post
}

function _run() {
  FUNCTION=$1
  docker run -p 9000:8080 "$FUNCTION"-lambda:latest --env OPENAI_API_KEY=$OPENAI_API_KEY --name "$FUNCTION"-lambda
}

function _clean() {
  docker rm -f "$FUNCTION"-lambda
}

function _push() {
  FUNCTION=$1
  aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
  docker tag "$FUNCTION-lambda:latest" "$AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/$FUNCTION-lambda:latest"
  docker push "$AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/$FUNCTION-lambda:latest"
}

# perform action with function
_$ACTION $FUNCTION