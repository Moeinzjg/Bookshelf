#!/bin/bash

config.sh

curl --data "token=$TOKEN&title=$1&author=$2&publisher=$3&genre=$4" $BASE_URL/submit/booksread/
