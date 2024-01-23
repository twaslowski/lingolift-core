#!/bin/bash

VERB=$1
FUNCTION=$2

VALID_BUILD_FUNCTIONS=("translation" "literal_translation" "syntactical_analysis" "response_suggestion")

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
  if [[ ! " ${VALID_BUILD_FUNCTIONS[@]} " =~ " ${FUNCTION} " ]]; then
      echo "Invalid function for build: $FUNCTION"
      echo "Valid functions are: ${VALID_BUILD_FUNCTIONS[*]}"
      exit 1
  fi

  # Slightly different build logic for different functions based on dependencies
  # Different files are required as well because otherwise imports would be failing
  case "$FUNCTION" in
      "translation"|"literal_translation"|"response_suggestion")
        export LAMBDA_FILE=lambda_functions_generative
        export DOCKERFILE=docker/Dockerfile-generative.template
        mkdir -p package
        poetry export -f requirements.txt --with generative -o package/requirements.txt --without-hashes
        ;;
      "syntactical_analysis")
        export LAMBDA_FILE=lambda_functions_nlp
        export DOCKERFILE=docker/Dockerfile-nlp.template
        mkdir -p package
        poetry export -f requirements.txt --with nlp -o package/requirements.txt --without-hashes
        ;;
      *)
          echo "Unhandled function: $FUNCTION"
          exit 1
          ;;
  esac

  sed "s/\$LAMBDA_HANDLER/${FUNCTION}_handler/g" $DOCKERFILE | sed "s/\$LAMBDA_FILE/${LAMBDA_FILE}/g" > Dockerfile
  docker build -t "${FUNCTION}-lambda" --platform linux/x86_64 .

  cleanup
}

function push() {
  FUNCTION=$1
  aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
  docker tag "$FUNCTION-lambda:latest" "$AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/$FUNCTION-lambda:latest"
  docker push "$AWS_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/$FUNCTION-lambda:latest"
}

# perform action with function
$VERB $FUNCTION