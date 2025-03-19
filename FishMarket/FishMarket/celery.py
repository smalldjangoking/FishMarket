import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FishMarket.settings')

app = Celery('FishMarket')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'run-my-function-every-day': {
        'task': 'novapost.tasks.novaposhta_api_initialization',
        'schedule': crontab(hour='22', minute='55'),
    },
}

