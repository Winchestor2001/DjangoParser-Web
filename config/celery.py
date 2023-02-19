import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'parse-web-every-30-minute': {
        'task': 'dparser.tasks.paser_web_1',
        'task': 'dparser.tasks.paser_web_2',
        'task': 'dparser.tasks.paser_web_3',
        'task': 'dparser.tasks.paser_web_4',
        'task': 'dparser.tasks.paser_web_5',
        'schedule': crontab(minute='*/30'),
    },
}
