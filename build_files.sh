#!/usr/bin/env bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput

# Ensure the output directory exists
mkdir -p vercel/output

# Move static files to the output directory (if needed)
cp -r staticfiles vercel/output/static

# Move your Django app to the output directory
cp -r * vercel/output/
