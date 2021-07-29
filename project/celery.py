from datetime import datetime, date
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.timezone = 'Asia/Almaty'

app.conf.beat_schedule = {
 'check_tasks': {
       'task': 'main.tasks.check_tasks',
       'schedule': crontab(hour=0, minute=0),
    },
}
