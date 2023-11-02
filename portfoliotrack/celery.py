from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfoliotrack.settings')

app = Celery('portfoliotrack')

app.conf.enable_utc = False

app.conf.update(timezone = 'America/Sao_Paulo')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))