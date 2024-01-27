ENV=$1

if [ -z "$ENV" ]; then
  echo "Usage: deploy.sh <env>"
  exit 1
fi

if [ "$ENV" != "dev" ] && [ "$ENV" != "prod" ]; then
  echo "Usage: deploy.sh <env>; env must be dev or prod"
  exit 1
fi

echo "Deploying to $ENV"
pushd terraform > /dev/null || exit 1

terraform init -backend-config="backend_${ENV}.hcl" -reconfigure
TF_VAR_environment="${ENV}" TF_VAR_commit_sha=$(git rev-parse --short HEAD) terraform apply -auto-approve

