from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialbuzz.settings')

app = Celery('socialbuzz')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'collect-pages-every-day-afernoon': {
        'task': 'facebook.tasks.collect_all_pages',
        'schedule': crontab(minute=0, hour=15),
        'args': (),
    },
    'collect-posts-every-day-afernoon': {
        'task': 'facebook.tasks.collect_all_posts',
        'schedule': crontab(minute=0, hour=15),
        'args': ()
    },
}

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
