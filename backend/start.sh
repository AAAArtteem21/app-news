#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py create_subscription_product
python manage.py fix_stripe_integration
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@admin.com', 'aaaaarteem21')"
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
