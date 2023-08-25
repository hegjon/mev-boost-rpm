#!/bin/sh

version="$1"
if [ -z "$version" ]; then
    echo "No version specific"
    exit 1
fi

rpmdev-bumpspec -c "Updated to version $version" -n "$version" besu.spec

git add besu.spec

git commit -m "Updated to version $version"
