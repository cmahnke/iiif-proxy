#!/bin/sh

if  [ -n "$1" ] ; then
    URL_PREFIX="$1"
else
    echo "No URL Prefix given!"
    exit 1
fi

if [ -r "$FILE_LIST" ] ; then
    while read IDENTIFIER; do
        echo "Requesting $URLPREFIX$IDENTIFIER"
        curl -sS -o /dev/null "$URLPREFIX$IDENTIFIER"
    done < "$FILE_LIST"
else
    echo "No file list!"
    exit 2
fi
