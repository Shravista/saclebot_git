#! /usr/bin/env python3
import rospy

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from scipy.spatial.transform import Rotation as TF
from std_msgs.msg import Float32
import numpy as np


class WashRoomEntry(object):
    def __init__(self):
        rospy.init_node("saclebot_entry")
        
        self.moveBot = rospy.Publisher("/cmd_vel", Twist,queue_size=1)
        self.laser_read = rospy.Subscriber("/scan",LaserScan,self.laser_callback)
        self.odom_read = rospy.Subscriber("/odom", Odometry,self.odom_call_back)
        self.yaw_pub = rospy.Publisher("/saclebot/yaw", Float32,queue_size=1)
        
        self.data= Float32()
        
        self.rate = rospy.Rate(10)
        self.cmd = Twist()
        self.ctrl_c = False
        rospy.on_shutdown(self.shutdownhook)
        
        self.ranges = 0
        self.angles = 0
        self.ranges_raw = 0
        self.angles_raw = 0
        self.x = 0
        self.y = 0
        self.yaw = 0
    
    def laser_callback(self,msg):
        ranges = msg.ranges
        delAng = msg.angle_increment
            
        angles_raw = np.arange(msg.angle_min, msg.angle_max,delAng)
        tmp = np.array(ranges)
        scan = tmp[tmp != np.inf]
        angles = angles_raw[tmp != np.inf]
        
        self.ranges = scan
        self.angles = angles
        self.ranges_raw = np.array(msg.ranges)
        self.angles_raw = angles_raw
    
    def odom_call_back(self,msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        temp = msg.pose.pose.orientation
        quat = np.array([temp.x, temp.y, temp.z, temp.w])
        temp = TF.from_quat(quat)
        yaw = temp.as_euler('zyx')[0]
        
        self.x = x
        self.y = y
        self.yaw = yaw
        self.data.data = np.rad2deg(yaw)
    
    def shutdownhook(self):
        self.ctrl_c = True
        self.cmd.linear.x = 0.0
        self.cmd.linear.y = 0.0
        self.cmd.linear.z = 0.0
        
        self.cmd.angular.x = 0.0
        self.cmd.angular.y = 0.0
        self.cmd.angular.z = 0.0
        
        self.moveBot.publish(self.cmd)
        rospy.logwarn("Robot has stopped due to shutdown!")
        rospy.logwarn("Shutting Down")
    
    def turn(self):
        while True:
            w = 1.5
            self.cmd.angular.z = w
            self.cmd.linear.x = 0.0
            self.moveBot.publish(self.cmd)
            
            self.yaw_pub.publish(self.data)
            self.rate.sleep()
        
    
    def straightline(self):
    
        v = 0.10
        w = 1.5
        i = 0
        while True:
            try:
                k = self.ranges.argmin()
                r_min = self.ranges[k]
                a_min = self.angles[k]
                
                bool_ind = np.abs(np.round(np.rad2deg(self.angles_raw))) == 90.0
                bool_ranges = np.isinf(self.ranges_raw[bool_ind])
                if np.sum(bool_ranges) == 4:
                    rospy.loginfo("Start turning")
                    angles_sum = np.sum(self.angles)
                    if angles_sum > 0:
                        w = abs(w)
                    else: 
                        w = -abs(w)
                                                
                    self.cmd.angular.z = w
                    self.cmd.linear.x = 0.0
                    self.moveBot.publish(self.cmd)
                else:
                    self.cmd.linear.x = v
                    self.cmd.angular.z = 0.0
                    self.moveBot.publish(self.cmd)
                    rospy.loginfo("Runnning Straight")
                
            except Exception as e:
                rospy.logdebug(e)
                r = self.ranges
                a = self.angles
                continue
            self.yaw_pub.publish(self.data)
            
            self.rate.sleep()

if __name__ == "__main__":
    ent = WashRoomEntry()
#    ent.straightline()
    ent.turn()
            
        
        
