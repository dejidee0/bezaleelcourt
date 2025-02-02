#!/usr/bin/env bash

echo "Build script starts executing..."
# exit on error
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
echo "Build script executed successfully."
