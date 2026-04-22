#!/bin/bash
python manage.py migrate --noinput
python -c "import django.contrib.admin; import os; print(os.path.join(os.path.dirname(django.contrib.admin.__file__), 'static'))"
python manage.py collectstatic --noinput -v 3 2>&1 | head -50
python manage.py create_subscription_product
python manage.py fix_stripe_integration
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3