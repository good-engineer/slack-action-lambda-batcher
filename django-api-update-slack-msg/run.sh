#!/bin/sh
# activate virtual enviroment
source env/bin/activate

# Load up .env
set -o allexport
[[ -f my_api/my_api/.env ]] && source my_api/my_api/.env
set +o allexport

# run the file
python3 api/manage.py runserver 0:8080