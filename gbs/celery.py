import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tine.settings')

app = Celery('tine')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
