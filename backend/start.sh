#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
python manage.py create_subscription_product
python manage.py fix_stripe_integration
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3