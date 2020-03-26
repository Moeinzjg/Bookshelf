#!/bin/bash

# please set below variables
TOKEN=123456789
BASE_URL="http:/localhost:8000"

curl --data "token=$TOKEN&title=$1&author=$2&publisher=$3&genre=$4" $BASE_URL/submit/books2read/
