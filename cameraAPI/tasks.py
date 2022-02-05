from __future__ import absolute_import, unicode_literals
import cv2
import os
from celery import shared_task
from cameraAPI.tasks import *
from cameraAPI.models import Camera
from celery.schedules import crontab
from skylarkTask.celery import app
from django.conf import settings
import cloudinary as cld
cld.config()

# @shared_task


@app.task
def change_image_per_5_minutes(camera_id):

    camera_obj = Camera.objects.get(id=int(camera_id))
    RTSP_URL = camera_obj.stream_url
    # print(RTSP_URL)
    cap = cv2.VideoCapture(RTSP_URL)
    ret, frame = cap.read()
    if cap.isOpened():
        _, frame = cap.read()
        cap.release()
        if _ and frame is not None:
            path = f'thumbnails/{camera_obj.owner.username}.jpg'
            cv2.imwrite('media/' + path, frame)
            # print("DONE WITH CV2")
            img_url = upload_to_cld('media/' + path)
            camera_obj.update_thumbnail(img_url)
            # delete cv2 temp image
            os.remove('media/' + path)
            # print("DONE")


def upload_to_cld(path):
    res = cld.uploader.upload(path, folder='media/thumbnails/', api_key=settings.CLOUDINARY_KEY,
                              api_secret=settings.CLOUDINARY_SECRET, cloud_name=settings.CLOUDINARY_CLOUD)
    # print(res)
    return res['secure_url']


dic = {}
for item in Camera.objects.all():
    dic['task'+str(item.id)] = {
        'task': 'cameraAPI.tasks.change_image_per_5_minutes',
        'schedule': crontab(minute='*/5'),
        'args': (item.id, )
    }

app.conf.beat_schedule = dic
