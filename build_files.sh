#!/usr/bin/env bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
