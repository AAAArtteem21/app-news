#!/bin/bash
python manage.py makemigrations
python manage.py migrate --noinput
cp -r /usr/local/lib/python3.10/site-packages/django/contrib/admin/static/admin /app/staticfiles/admin
ls -la /app/staticfiles/
python manage.py create_subscription_product
python manage.py fix_stripe_integration
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3