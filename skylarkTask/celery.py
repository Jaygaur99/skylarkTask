from __future__ import absolute_import, unicode_literals
from msilib import add_tables

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylarkTask.settings')

app = Celery('skylarkTask', broker='redis://localhost')

app.config_from_object('django.conf:settings', namespace='CELERY')



app.autodiscover_tasks()

