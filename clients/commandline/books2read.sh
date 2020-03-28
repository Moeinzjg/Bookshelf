#!/bin/bash

source config.sh

print_usage()
{
    echo "Use this script to submit books read to $(BASE_URL)"
    echo "Usage: ${0} <title> <author> <publisher> <genre> Eg."
    echo "Usage: ${0} 'a fraction of whole' 'Steve Toltz' 'cheshme' 'gray comedy'"
}

TITLE=$1

if [ -z "$TITLE" ]; then
    print_usage
    read -p "Press enter to exit"
    exit 1
fi

curl --data "token=$TOKEN&title=$TITLE&author=$2&publisher=$3&genre=$4" $BASE_URL/submit/books2read/

read -p "Press enter to exit"