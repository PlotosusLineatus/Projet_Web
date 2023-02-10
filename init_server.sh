#!/bin/sh


## INITIALIZE SERVER 

rm db.sqlite3
rm -rf genomeBact/migrations/*

python3 manage.py runscript reset_db

# For some reason, reset_db sometine needs to 
# be ran twice in order to properly work 
exit_code=$?

if [ $exit_code -ne 0 ]; then
    python3 manage.py runscript reset_db
else
    echo "Databse reset script ran successfully"
fi
python3 manage.py runscript create_groups
python3 manage.py runserver
