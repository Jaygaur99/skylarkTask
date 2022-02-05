from __future__ import absolute_import, unicode_literals
from msilib import add_tables

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylarkTask.settings')

app = Celery('skylarkTask', broker='redis://localhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from cameraAPI.models import Camera
    from cameraAPI.tasks import change_image_per_5_minutes
    # dic = {}
    for obj in Camera.objects.all():
        # dic['change_image_per_5_minutes' + str(obj.id)] = {
        #     'task': 'cameraAPI.tasks.change_image_per_5_minutes',
        #     'schedule': 10, # crontab(minute=5),
        #     'args': (obj,)
        # }
        sender.add_periodic_task(10.0, change_image_per_5_minutes.s('hello'), name='change_image_per_5_minutes' + str(obj.id))
    # print(dic)
    # app.conf.beat_schedule = dic

# app.conf.schedule_beat = configure_periodic_tasks()

app.autodiscover_tasks()