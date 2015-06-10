
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
   bin="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
   SOURCE="$(readlink "$SOURCE")"
   [[ $SOURCE != /* ]] && SOURCE="$bin/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
scripts="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

if [ "$#" -ne 2 ]; then
  echo "Usage: gen-javadoc.sh <releaseVersion> <pathToFluoCode>"
  exit 1
fi

RELEASE_VERSION=$1
FLUO_PATH=$2

RELEASE_DOCS=$scripts/../apidocs/$RELEASE_VERSION

if [ -d "$RELEASE_DOCS" ]; then
  echo "API docs directory already exists at $RELEASE_DOCS"
  exit 1
fi

mkdir -p $RELEASE_DOCS

cd $FLUO_PATH
git checkout $RELEASE_VERSION
mvn clean javadoc:aggregate
cp -r target/site/apidocs $RELEASE_DOCS/full

cd modules/api
mvn clean javadoc:aggregate
cp -r target/site/apidocs $RELEASE_DOCS/api
