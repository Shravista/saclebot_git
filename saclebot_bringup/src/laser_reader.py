#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
from numpy import sin, cos, pi
import matplotlib.pyplot as plt
import time

DF = []
def callback(msg):
    global DF
    ranges = msg.ranges
    delAng = msg.angle_increment
        
    angles = np.arange(msg.angle_min, msg.angle_max,delAng)
    tmp = np.array(ranges)
    scan = tmp[tmp != np.inf]
    angles = angles[tmp != np.inf]
    scan = scan.reshape(-1,1)
    df = np.diff(scan,axis=0)

    DF.append(df)
    np.save('df1.npy',DF)
    rospy.loginfo("I am here!!!!:  "+str(len(DF)))
rospy.init_node("laser_test")     
subs = rospy.Subscriber("/scan",LaserScan,callback)
print(len(DF))
rospy.spin()
