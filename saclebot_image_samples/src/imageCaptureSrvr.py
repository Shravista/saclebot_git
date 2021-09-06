#! /usr/bin/env python3

import rospy
import numpy as np
import cv2
from saclebot_image_samples.srv import ImageCaptureSrvMessage, ImageCaptureSrvMessageRequest

rospy.init_node("imageCaptureSerivceClient")
rospy.wait_for_service("/saclebot/realsense2_d435i/image_capture")

client = rospy.ServiceProxy("/saclebot/realsense2_d435i/image_capture",ImageCaptureSrvMessage,persistent=True)
rqt = ImageCaptureSrvMessageRequest()
msg = "show"
num = 0
write = True
rate = rospy.Rate(1)
ctrl_c = False

def shutdownhook():
    global ctrl_c
    print("shutdown time")
    client.close()
    ctrl_c = True
    
rospy.on_shutdown(shutdownhook)
while not ctrl_c:
    rospy.loginfo("Requesting a service")
    
    save = input()
    try:
        num = int(save)
    except:
        ctrl_c = True
    rqt.msg = msg
    rqt.num = num
    rqt.write = write
    try:
        h = client(rqt)
    except Exception as e:
        print(e)
        ctrl_c = True
    print(h)
    rate.sleep()

