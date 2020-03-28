#!/bin/bash

source config.sh

STAT=$(curl --data "token=$TOKEN" $BASE_URL/query/generalstat/)

echo "$STAT"

read -p "Press enter to exit"