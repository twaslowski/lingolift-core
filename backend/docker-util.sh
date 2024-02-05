#!/bin/bash

VERB=$1
FUNCTION=$2
ENV=$3

VALID_BUILD_FUNCTIONS=("translation" "literal_translation" "syntactical_analysis" "response_suggestion" "inflection")

if [ -z "$VERB" ]; then
  echo "Missing action."
  exit 1
fi

function cleanup() {
  rm -rf package
  rm -f Dockerfile
}

function build() {
  FUNCTION=$1

  # assume that only functions within lambda_functions_nlp would have to be dockerized due to their usage of spacy
  export LAMBDA_FILE=lambda_functions_nlp
  export DOCKERFILE=Dockerfile-nlp.template

  # create temporary directory to store relevant build files for Dockerfile
  mkdir -p package
  poetry export -f requirements.txt --with nlp --with generative -o package/requirements.txt.tmp --without-hashes

  # poetry exports the path to the shared package as an absolute path on my file system
  # that obviously does not work with docker, so when packaging, the shared package is simply manually copied
  # into the root of the docker workdir, which is what the updated requirements.txt file reflects
  sed 's/^shared.*$/.\/shared/g' package/requirements.txt.tmp > package/requirements.txt
  cp -r ../shared/ package/shared/

  sed "s/\$LAMBDA_HANDLER/${FUNCTION}_handler/g" $DOCKERFILE | sed "s/\$LAMBDA_FILE/${LAMBDA_FILE}/g" > Dockerfile
  docker build -t "${FUNCTION}-lambda" --no-cache --platform linux/x86_64 .

  cleanup
}

function push() {
  FUNCTION=$1
  commit_sha=$(git rev-parse --short HEAD)
  aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com"
  docker tag "$FUNCTION-lambda:latest" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/${FUNCTION}-lambda-${ENV}:latest"
  docker tag "$FUNCTION-lambda:latest" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/${FUNCTION}-lambda-${ENV}:${commit_sha}"
  docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/${FUNCTION}-lambda-${ENV}:latest"
  docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-central-1.amazonaws.com/${FUNCTION}-lambda-${ENV}:${commit_sha}"
}

# perform action with function
$VERB "${FUNCTION}"