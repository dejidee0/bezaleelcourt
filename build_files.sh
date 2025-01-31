#!/usr/bin/env bash

python3.9 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

# Collect static files
python3.9 manage.py collectstatic --noinput
