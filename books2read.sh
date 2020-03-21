#!/bin/bash

mytoken=123456789

curl --data "token=$mytoken&title=$1&author=$2&publisher=$3&genre=$4" http://localhost:8000/library/submit/books2read/
