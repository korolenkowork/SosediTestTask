#!/bin/sh
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Collecting Test Data..."
python manage.py createtestcollections 100
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
