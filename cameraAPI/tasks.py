from __future__ import absolute_import, unicode_literals
import cv2
import os
from celery import shared_task
from cameraAPI.tasks import *
from cameraAPI.models import Camera
from celery.schedules import crontab
from skylarkTask.celery import app
import cloudinary as cld
cld.config()

# @shared_task
@app.task
def change_image_per_5_minutes(camera_obj):
    # RTSP_URL = 'rtsp://10.5.36.206:5554/playlist.m3u'
    # print(camera_obj.id)
    print("HUI")
    RTSP_URL = camera_obj.stream_url
    print(RTSP_URL)
    cap = cv2.VideoCapture(RTSP_URL)
    ret, frame = cap.read()
    if cap.isOpened():
        _, frame = cap.read()
        cap.release()
        if _ and frame is not None:
            path = f'thumbnails/{camera_obj.owner.username}.jpg'
            cv2.imwrite('media/' + path, frame)
            img_url = upload_to_cld('media/' + path)
            camera_obj.update_thumbnail(img_url)
            # delete cv2 temp image
            os.remove('media/' + path)


def upload_to_cld(path):
    res = cld.uploader.upload(path, folder='media/thumbnails/', api_key='938331574129682',
                        api_secret="VOBykdG82qjUVNMgelDBkry4bcM", cloud_name="dpzcldoy7")
    return res['secure_url']
# def configure_periodic_tasks():
#     dic = {}
#     for obj in Camera.objects.all():
#         dic['change_image_per_5_minutes' + str(obj.id)] = {
#             'task': 'cameraAPI.tasks.change_image_per_5_minutes',
#             'schedule': 10, # crontab(minute=5),
#             'args': (obj,)
#         }
#     print(dic)
#     app.conf.beat_schedule = dic
