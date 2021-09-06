#! /usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from saclebot_image_samples.srv import ImageCaptureSrvMessage, ImageCaptureSrvMessageResponse
import rospkg

class ImageCapture(object):
    def __init__(self,node_name,topic):
        rospy.init_node(node_name)
        self.imgCapSvc = rospy.Service("/saclebot/realsense2_d435i/image_capture",ImageCaptureSrvMessage, self.srvCallback)
        self.img_default = Image()
        self.topic = topic
        self.ctrl_c = False
        self.subs = rospy.Subscriber(self.topic,Image,self.img_callback)
        rospy.on_shutdown(self.shutdownhook)
        self.rate = rospy.Rate(1)
        self.bridge = CvBridge()
        self.img = np.array([])
        self.response = ImageCaptureSrvMessageResponse()
    
    def shutdownhook(self):
        self.ctrl_c = True
        rospy.loginfo("Shutting Down")
    
    def srvCallback(self,request):
        I = self.getImage()
        rqt = request
        i = request.num
        rospack = rospkg.RosPack()
        path = rospack.get_path("saclebot_image_samples")
        if rqt.msg == "show":
            rospy.loginfo("Your request for the showing image is under process")
            cv2.imshow('img',I)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.response.response = "Image has shown and "
            rospy.loginfo("Your request for showing image is successful")
        else:
            rospy.logwarn("Not requested any thing desrired by the author")
            self.response.response = "Image is not shown"
        if rqt.write:
            rospy.loginfo("Your request for writing for image to .jpg file is underway")
            path +="/images/img_"+str(i)+".jpg"
            print(path)
            a = cv2.imwrite(path,I)
            self.response.response += "Image is written to the file " + f"img_{i}" + ".jpg"
            rospy.loginfo("Your request for writing for image to .jpg is successful or "+ str(a))
        else:
            rospy.loginfo("Your request for not writing the image to a file is successful")
            self.response.response += "Image is not written"
        
        self.response.success = True
#        self.response.data = I
        return self.response
        
    def img_callback(self,msg):
        self.img_default = msg
        try: 
            cv_img = self.bridge.imgmsg_to_cv2(self.img_default,"rgb8")
            self.img = cv_img
        except Exception as e:
            rospy.logerr(e)            
    
    def getImage(self):return self.img
    
    def imageSubs(self):
        
        while not self.ctrl_c:
            i = 1
#            rospy.loginfo("I have subscribed to this topic for once I guess")
#            self.rate.sleep()


if __name__ == "__main__":
    sub = ImageCapture("img_cap","/realsense2_d435i/rgb/image_raw")
    rospy.spin()
    
    
