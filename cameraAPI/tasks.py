from __future__ import absolute_import, unicode_literals
from celery import shared_task 
import cv2


@shared_task
def change_image_per_5_minutes(camera_obj):
    # RTSP_URL = 'rtsp://10.5.36.206:5554/playlist.m3u'
    # print(camera_obj.id)
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
            camera_obj.update_thumbnail( '/' + path)    
