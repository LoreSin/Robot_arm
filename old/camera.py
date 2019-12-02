import cv2
import sys
gst_str = ('nvarguscamerasrc !' 
    'video/x-raw(memory:NVMM), '
    'width=1280, height=720, '
    'format=NV12, framerate=30/1 ! '
    'nvvidconv ! '
    'video/x-raw, format=BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=BGR ! appsink')

'video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=120/1'





cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print('Failed to open camera!')
    sys.exit()
while(True):
    _, img = cap.read() # grab the next image frame from camera
    cv2.imshow("cam", img)
    key = cv2.waitKey(10)
