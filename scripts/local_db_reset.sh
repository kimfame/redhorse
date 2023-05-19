#!/bin/bash

activate() {
  echo "Activate virtualenv..."
  . venv/bin/activate
}

echo "Reset local DB (SQLite)"

# Move project root folder
SCRIPT_FILE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
cd $SCRIPT_FILE_PATH
cd ..

activate

echo "Remove db.sqlite3"
rm db.sqlite3

echo "Remove profile pictures"
rm -rf media/profile_picture

echo "Make migrations"
python3 manage.py makemigrations

echo "Migrate"
python3 manage.py migrate

echo "Set base data"
python3 manage.py runscript scripts.base_data_generator

echo "Set dev data"
python3 manage.py runscript scripts.dev_data_generator

echo "Finished."