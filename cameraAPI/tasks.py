import cv2
import os
 
RTSP_URL = 'rtsp://10.4.235.137:5554/playlist.m3u'
 
# os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
 
cap = cv2.VideoCapture(RTSP_URL)
 
# if not cap.isOpened():
#     print('Cannot open RTSP stream')
#     exit(-1)
 
# while True:
#     _, frame = cap.read()
#     cv2.imshow('RTSP stream', frame)
 
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

ret, frame = cap.read()

if cap.isOpened():
    _, frame = cap.read()
    cap.release()
    if _ and frame is not None:
        cv2.imwrite('latest.jpg', frame)
        print("OK")
    print("OK2")
print("OOK")
 
