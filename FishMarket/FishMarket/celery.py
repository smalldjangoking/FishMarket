import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FishMarket.settings')

app = Celery('FishMarket')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()