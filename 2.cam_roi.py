import cv2
import numpy as np

cam = cv2.VideoCapture(1)

while True:
    ret, frame = cam.read()

    # ROI Setting
    roi_width_size = 100
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


    # get Color from ROI with histogram (range of blue & red)
    roi_img_hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
    lower_red = (0, 100, 100)
    upper_red = (180, 255, 255)
    mask = cv2.inRange(roi_img_hsv, lower_red, upper_red)

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
    hue_threshold_rate = 0.8
    if ((hue_max <= 15) or (165 <= hue_max)) and (rate_hue_r > hue_threshold_rate):
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 255, 255))
    elif (105 <= hue_max <= 135) and (rate_hue_b > hue_threshold_rate):
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 255, 255))
    else:
        temp_color_img = np.full_like(roi_img_hsv, (hue_max, 0, 0))


    # output images
    # cv2.imshow('cam', frame)
    cv2.imshow('cam', img_roi_drawing)
    cv2.imshow('Region of Interest', roi_img)
    cv2.imshow('ROI MAX COLOR', cv2.cvtColor(
        temp_color_img, cv2.COLOR_HSV2BGR))


    # process key input
    key = cv2.waitKey(25)
    if key < 0:
        continue
    elif key == 27:
        break
    else:
        pass



cv2.destroyAllWindows()

