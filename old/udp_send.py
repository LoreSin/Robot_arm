import socket
import numpy as np
import cv2 as cv


addr = ("192.168.0.30", 65534)
buf = 512
width = 640 // 2
height = 480 // 2
cap = cv.VideoCapture(1)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while(cap.isOpened()):
        ret, frame = cap.read()
        img_for_udp = cv.resize(frame, (320, 240))
        if ret:
            s.sendto(code, addr)
            data = img_for_udp.tostring()
            print(len(data), img_for_udp.shape)
            for i in range(0, len(data), buf):
                s.sendto(data[i:i+buf], addr)
#            cv.imshow('send', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
