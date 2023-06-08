from __future__ import division
import os
import time
import cv2
import win32api
import win32con
import dlib
from if_blinking import blinking_ratio_1,list_ratio,excute_parallel,excute_vertical,blinking_ratio_2
webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW)#调用摄像头
eye_states = []#blinking 1,gaze 0

head_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 返回训练好的人脸68特征点检测器
#eye_predictor = dlib.shape_predictor('eye_eyebrows_22.dat')
head_detector = dlib.get_frontal_face_detector()
blinking_ratios_left = []
blinking_ratios_right = []
ratio_list_left = [1,1,1,1,1]
ratio_list_right = [1,1,1,1,1]
xs= []
ys = []
first = 0
num = 0
nums = []
while True:
    _, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = head_detector(frame)
    try:
        landmarks = head_predictor(frame, faces[0])  # return the landmarks of the face
        #landmarks_eye = eye_predictor(frame,faces[0])
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0,0,255), 2)
        for index, pt in enumerate(landmarks.parts()):
            pt_pos = (pt.x, pt.y)
            cv2.circle(frame, pt_pos, 1, (255, 0, 0), 1)
            # cv2.putText(frame,str(index),pt_pos,cv2.FONT_HERSHEY_DUPLEX, 0.3, (0,0,255), 1)
        ratio_left = blinking_ratio_1(landmarks,0)
        ratio_right = blinking_ratio_1(landmarks,1)
        #print(ratio_right,ratio_left)
        # ratio_left_2 = blinking_ratio_2(landmarks_eye, 0)
        # ratio_right_2 = blinking_ratio_2(landmarks_eye, 1)
        # ratio_list_left,l_avg = list_ratio(ratio_list_left,ratio_left)
        # ratio_list_right,r_avg = list_ratio(ratio_list_right,ratio_right)
        x,y = excute_parallel(landmarks),excute_vertical(landmarks)
        if x < 0.4:
            parallel_direction = -3
            text1 = "left"
        if x < 0.5 and x > 0.4:
            parallel_direction = -1
            text1 = "light left"
        if x > 0.5 and x <2:
            parallel_direction = 0
            text1 = "center"
        if x >2 and x < 4:
            parallel_direction = 1
            text1 = "light right"
        if  x > 4:
            parallel_direction = 3
            text1 = "right"

        text2 = ''
        if y > 0.5 and y < 0.7:
            vertical =0
            text2 = 'center'
        if y <0.5:
            vertical = 2
            text2 = 'up'
        if y <0.4:
            vertical = 4
            text2 = 'up'
        if y > 0.7:
            vertical = -2
            text2 = 'down'
        if y > 0.75:
            vertical = -4
        text = text1 +str(round(x,2))+text2+str(round(y,2))
        xs.append(x)
        ys.append(y)
        num = num + 1
        nums.append(num)
        #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -4*parallel_direction, -4*vertical)
        # else:
        #     text = "gaze"
        # blinking_ratios_left.append(ratio_left)
        # blinking_ratios_right.append(ratio_right)

        # if ratio_right > 4.7 and ratio_left > 4.7:#判断是否在眨眼
        #
        #     eye_states.append(first)
        #     if time.time()-first<0.6 and time.time()-first>0.2:
        #         # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        #         # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        #         text = "double click"
        #         print(text)
        #     # elif eye_states[-1] - eye_states[-5] <0.2:
        #     #     print('drag')
        #         # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        #
        #     first = time.time()
        # else:
        #     # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        #     text = 'gaze'
        #
        #print(text, ratio_right_2, ratio_left_2)
        # if ratio_right - ratio_left>=0.8 :#判断左眼是否眨眼
        #     text = "left blinking"
        #     print(text, ratio_right, ratio_left)
        # elif ratio_left - ratio_right>=0.7 :#判断右眼是否眨眼
        #     text = "right blinking"
        #     print(text, ratio_right, ratio_left)
    except:
        text = "None head"
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
webcam.release()
cv2.destroyAllWindows()
import matplotlib.pyplot as plt
#plt.plot(nums, xs, "g", label="水平转向")
plt.plot(nums, ys, "r", label="垂直转向")
plt.show()
def value_head(frames):
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = head_detector(frames)
    try:
        landmarks = head_predictor(frames, faces[0])
        x, y = excute_parallel(landmarks), excute_vertical(landmarks)
        return x,y
    except:
        return None