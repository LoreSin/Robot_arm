from functools import partial
import cv2
import numpy as np
import socket

from control import move_to_right_area, move_to_left_area, clean_GPIO


# Setting cam & UDP
cam = cv2.VideoCapture(1)

addr = ("192.168.0.30", 65534)
buf = 512
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')
udp_img_size_width, udp_img_size_height = 320, 240
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
operating_robot = False
counter = 0
counter_threshold = 40 # 1 to 25 ms 40 to 1 sec

while (cam.isOpened()):
    ret, frame = cam.read()

    # ROI Setting
    roi_width_size = 50
    roi_height_size = 100

    frame_height, frame_width = frame.shape[:2]
    if (frame_height < roi_height_size) or (frame_width < roi_width_size):
        print('roi size over image size')
        break

    center_height, center_width = frame_height // 2, frame_width // 2
    pt1 = center_width - roi_width_size // 2, center_height - roi_height_size // 2
    pt2 = center_width + roi_width_size // 2, center_height + roi_height_size // 2
    roi_range_x = slice(pt1[0], pt2[0])
    roi_range_y = slice(pt1[1], pt2[1])

    roi_img = frame[roi_range_y, roi_range_x].copy()
    img_roi_drawing = cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)
    putText = partial(cv2.putText, org= (0, frame_height),fontFace=cv2.FONT_HERSHEY_SIMPLEX , fontScale=1.5, thickness=5)


    # get Color from ROI with histogram (range of blue & red)
    roi_img_hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
    lower_color = (0, 20, 20)
    upper_color = (180, 255, 255)
    mask = cv2.inRange(roi_img_hsv, lower_color, upper_color)

    hist1 = cv2.calcHist([roi_img_hsv], [0], mask, [180], [0, 180])
    hue_max = np.argmax(hist1)
    hue_r = np.sum(hist1[:15]) + np.sum(hist1[165:])
    hue_g = np.sum(hist1[30:90])
    hue_b = np.sum(hist1[105:135])
    roi_img_size = roi_img.shape[0] * roi_img.shape[1]

    rate_hue_r = hue_r / roi_img_size
    rate_hue_g = hue_g / roi_img_size
    rate_hue_b = hue_b / roi_img_size
    print(f'{hue_max:3}, red: {rate_hue_r * 100:2.1f}%, green: {rate_hue_g * 100:2.1f}% , blue: {rate_hue_b * 100:2.1f}%')


    # process color
    hue_threshold_rate = 0.6

    if ((hue_max <= 15) or (165 <= hue_max)) and (rate_hue_r > hue_threshold_rate):
        counter += 1
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 255, 255))
        text_color = (0,0,255)
        if not operating_robot and counter > counter_threshold:
            counter = 0
            operating_robot = True
            move_to_right_area()
            operating_robot = False

    elif (105 <= hue_max <= 135) and (rate_hue_b > hue_threshold_rate):
        counter += 1
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 255, 255))
        text_color = (255,0,0)
        if not operating_robot and counter > counter_threshold:
            counter = 0
            operating_robot = True
            move_to_blue_area()
            operating_robot = False

    else:
        counter = 0
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 0, 0))
        text_color = (0,0,0)
    putText(img_roi_drawing, f'RED: {100*rate_hue_r:00.1f}% BLUE: {100*rate_hue_b:00.1f}%', color=text_color)

    # output images
    # cv2.imshow('cam', frame)
    # cv2.imshow('cam', img_roi_drawing)
    # cv2.imshow('Region of Interest', roi_img)
    # cv2.imshow('ROI MAX COLOR', cv2.cvtColor(temp_color_img, cv2.COLOR_HSV2BGR))


    # send image to udp
    img_for_udp = cv2.resize(img_roi_drawing, (320, 240))
    if ret:
        s.sendto(code, addr)
        data = img_for_udp.tostring()
        # print(len(data), img_for_udp.shape)
        for i in range(0, len(data), buf):
            s.sendto(data[i:i+buf], addr)
        # cv2.imshow('send', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
            # break


    # process key input
    key = cv2.waitKey(25)
    if key < 0:
        continue
    elif key == 27:
        break
    else:
        pass

clean_GPIO()
cv2.destroyAllWindows()
