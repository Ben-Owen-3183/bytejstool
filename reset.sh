parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
rm -rf ../testing/working_code/*
cp -R ../testing/example_code/* ../testing/working_code