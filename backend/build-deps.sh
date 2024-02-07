DEPENDENCY_GROUP=$1
PACKAGE_DIRECTORY="package_${DEPENDENCY_GROUP}_deps"
# Creates a package for a Poetry dependency group, to be uploaded as a Lambda layer.

if [ -z "$DEPENDENCY_GROUP" ]; then
    echo "Usage: $0 <group>"
    exit 1
fi

mkdir -p "${PACKAGE_DIRECTORY}/python/lib/python3.11/site-packages"
poetry export --with "${DEPENDENCY_GROUP}" -f requirements.txt -o "${PACKAGE_DIRECTORY}/requirements.txt" --without-hashes

python3.11 -m pip install -r "${PACKAGE_DIRECTORY}/requirements.txt" \
  --target "${PACKAGE_DIRECTORY}/python/lib/python3.11/site-packages" \
  --platform manylinux2014_x86_64 --only-binary=:all:

cd "${PACKAGE_DIRECTORY}" && zip -r "../${PACKAGE_DIRECTORY}.zip" . && cd ..
