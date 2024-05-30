#!/usr/bin/env bash
# exit on error
set -o errexit

python3 -m pip3 install --upgrade pip3

pip3 install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
