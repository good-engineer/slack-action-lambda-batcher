#!/bin/sh
# activate virtual enviroment
source env/bin/activate

# Load up .env
set -o allexport
[[ -f .env ]] && source .env
set +o allexport

# run the file
python3 main.py