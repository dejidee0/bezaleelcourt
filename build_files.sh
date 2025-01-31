#!/usr/bin/env bash

set -e  # Exit on error

echo "Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating output directory..."
mkdir -p vercel/output

echo "Moving static files..."
cp -r static vercel/output/static

echo "Moving Django app files..."
cp -r * vercel/output/

echo "Build script executed successfully."
