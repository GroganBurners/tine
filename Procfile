release: python manage.py makemigrations && python manage.py migrate --noinput
web: gunicorn tine.wsgi:application -w 2 -b :5000 --reload --log-level DEBUG
worker: celery -A gbs worker -l INFO
beat: celery -A gbs beat
