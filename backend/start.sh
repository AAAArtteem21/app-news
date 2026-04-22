#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py create_subscription_product
python manage.py fix_stripe_integration
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='admin')
u.set_password('admin123')
u.save()
"
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3