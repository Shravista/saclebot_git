#! /usr/bin/env python3

import rospy 
from std_msgs.msg import Float64
rospy.init_node("saclebot_setting_home_states")

R3_pub = rospy.Publisher("/R3_joint_position_controller/command",Float64, queue_size=1)
camera_pub = rospy.Publisher("/camera_head_joint_position_controller/command", Float64, queue_size=1)
slider_pub = rospy.Publisher("/slider_joint_position_controller/command", Float64, queue_size=1)

cmd = Float64()
cmd1 = Float64()
cmd1.data = 0.8
cmd.data = 0.0
i = 0
rate = rospy.Rate(1)

rospy.loginfo("Setting the saclebot home states")
while i <3:

    R3_pub.publish(cmd)
    camera_pub.publish(cmd)
    slider_pub.publish(cmd1)
    rate.sleep()
    i+=1

rospy.loginfo("SacleBot is in Home state!!!")
