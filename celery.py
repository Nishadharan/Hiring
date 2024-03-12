# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HiringBackend.settings')

# create a Celery instance and configure it using the settings from Django
app = Celery('HiringBackend')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'call-api-task': {
        'task': 'your_app.tasks.call_api_task',
        'schedule': 30.0,  # Set the interval in seconds
    },
}
app.conf.timezone = 'UTC'