#!/usr/bin/env bash
# exit on error
set -o errexit

source venv/bin/activate

python3 -m pip install --upgrade pip

pip install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
