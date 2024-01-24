DEPENDENCY_GROUP=$1

# Creates a package for a Poetry dependency group, to be uploaded as a Lambda layer.

if [ -z "$DEPENDENCY_GROUP" ]; then
    echo "Usage: $0 <group>"
    exit 1
fi

mkdir -p "package_${DEPENDENCY_GROUP}/python/lib/python3.11/site-packages"
poetry export --only "${DEPENDENCY_GROUP}" -f requirements.txt -o "package_${DEPENDENCY_GROUP}/requirements.txt" --without-hashes

python3.11 -m pip install -r "package_${DEPENDENCY_GROUP}/requirements.txt" \
  --target "package_${DEPENDENCY_GROUP}/python/lib/python3.11/site-packages" \
  --platform manylinux2014_x86_64 --only-binary=:all:

