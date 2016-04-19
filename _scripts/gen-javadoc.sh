
if [ "$#" -ne 3 ]; then
  echo "Usage: gen-javadoc.sh <releaseVersion> <pathToCode> <pathToJavadocs>"
  exit 1
fi

RELEASE_VERSION=$1
CODE_PATH=$2
DOCS_PATH=$3
RELEASE_PATH=$3/$1

if [ ! -d "$CODE_PATH" ]; then
  echo "Code directory does not exist at $CODE_PATH"
  exit 1
fi
if [ ! -d "$DOCS_PATH" ]; then
  echo "Base API docs directory does not exist at $DOCS_PATH"
  exit 1
fi

if [ -d "$RELEASE_PATH" ]; then
  echo "Release API docs directory already exists at $RELEASE_DOCS"
  exit 1
fi

cd $CODE_PATH
git checkout $RELEASE_VERSION
mvn clean javadoc:aggregate
cp -r target/site/apidocs $RELEASE_PATH
