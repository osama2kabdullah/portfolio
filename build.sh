#!/bin/bash
set -e
pip install -r requirements.txt
apt-get update && apt-get install -y build-essential
python manage.py migrate --noinput
python manage.py collectstatic --noinput
