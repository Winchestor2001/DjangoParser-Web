import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

hours = 1

app.conf.beat_schedule = {
    f'parse-web-1-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_1',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-2-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_2',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-3-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_3',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-4-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_4',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-5-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_5',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-6-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_6',
        'schedule': crontab(hour=f'*/{hours}'),
    },
    f'parse-web-7-every-{hours}-minute': {
        'task': 'dparser.tasks.paser_web_7',
        'schedule': crontab(hour=f'*/{hours}'),
    },

}
