#!/usr/bin/env bash

echo "Build script starts executing..."
# exit on error
set -o errexit
# pip install -r requirements.txt
# python manage.py collectstatic --no-input
# python manage.py collectstatic --noinput

# python manage.py migrate
# echo "Build script executed successfully."


echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Applying migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating output directory..."
mkdir -p render/output

echo "Moving static files..."
cp -r staticfiles render/output/static  # Ensure 'staticfiles' is correct


echo "Build script executed successfully."
