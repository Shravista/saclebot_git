#! /usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from saclebot_image_samples.srv import ImageSrvMessage, ImageSrvMessageResponse

bridge = CvBridge()

def callback(msg):
    print("I am here")
    try: 
        cv_img = bridge.imgmsg_to_cv2(msg,"rgb8")
    except Exception as e:
        rospy.logerr(e)     
    print(cv_img.shape)
    cv2.imshow('img',cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("images/img.jpg",cv_img)

rospy.init_node("Hii")
print("I am below node init")
sub = rospy.Subscriber("/realsense2_d435i/rgb/image_raw",Image,callback)
rospy.spin()
