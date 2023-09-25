while [[ $# -gt 0 ]]; do
  case $1 in
    --build)
      export REBUILD_DOCKER=true
      shift
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

# check that .env exists
if [ ! -f .env ]; then
  echo "Error: .env file does not exist." >&2
  exit 1
else
  echo ".env file exists; sourcing ..."
  source .env
fi

# run mongodb docker image
docker ps --format '{{.Names}}' | grep -q lingolift-backend
if [ "$?" -eq 0 ]; then
  echo "backend already running"
  if [[ -n $REBUILD_DOCKER ]]; then
    docker build -t lingolift-backend:latest .
    docker stop lingolift-backend
    docker run -p 5001:5000 -d --env OPENAI_API_KEY=$OPENAI_API_KEY lingolift-backend:latest
  fi
else
  docker run -p 5001:5000 -d --env OPENAI_API_KEY=$OPENAI_API_KEY lingolift-backend:latest
fi

# run frontend
pushd frontend
ng serve --host=0.0.0.0