#! /usr/bin/env python3

import rospy
from std_srvs.srv import Trigger, TriggerRequest
import numpy as np


rospy.init_node("saclebot_spawn_request")
rospy.wait_for_service("/saclebot/relocate_trash")

client = rospy.ServiceProxy("/saclebot/relocate_trash",Trigger)

req = TriggerRequest()
try:
    X = [1.5,2.0,0.8,0.75]
    Y = [1.5,2.0,0.8,0.75]
    roll = [np.pi/2,0,-np.pi/2]
    pitch = [np.pi/2,0,-np.pi/2]
    yaw = [np.pi/2,0,-np.pi/2]
    #("---------------Pose for the red cup---------------")
    cng = np.random.default_rng(123456789)
    print(type(float(X[np.random.randint(0,4)])))
    rospy.set_param("/saclebot_red_paper_cup_pose_config/X",X[np.random.randint(0,4)])
    rospy.set_param("/saclebot_red_paper_cup_pose_config/Y",Y[np.random.randint(0,4)])
    rospy.set_param("/saclebot_red_paper_cup_pose_config/roll",roll[np.random.randint(0,3)])
    rospy.set_param("/saclebot_red_paper_cup_pose_config/pitch",pitch[np.random.randint(0,3)])
    rospy.set_param("/saclebot_red_paper_cup_pose_config/yaw",yaw[np.random.randint(0,3)])
    
    #("---------------Pose for the green cup---------------")
    rospy.set_param("/saclebot_green_paper_cup_pose_config/X",X[np.random.randint(0,4)])
    rospy.set_param("/saclebot_green_paper_cup_pose_config/Y",Y[np.random.randint(0,4)])
    rospy.set_param("/saclebot_green_paper_cup_pose_config/roll",roll[np.random.randint(0,3)])
    rospy.set_param("/saclebot_green_paper_cup_pose_config/pitch",pitch[np.random.randint(0,3)])
    rospy.set_param("/saclebot_green_paper_cup_pose_config/yaw",yaw[np.random.randint(0,3)])
    
    #("---------------Pose for the coke can---------------")
    rospy.set_param("/saclebot_coke_can_pose_config/X",X[np.random.randint(0,4)])
    rospy.set_param("/saclebot_coke_can_pose_config/Y",Y[np.random.randint(0,4)])
    rospy.set_param("/saclebot_coke_can_pose_config/roll",roll[np.random.randint(0,3)])
    rospy.set_param("/saclebot_coke_can_pose_config/pitch",pitch[np.random.randint(0,3)])
    rospy.set_param("/saclebot_coke_can_pose_config/yaw",yaw[np.random.randint(0,3)])
    
    res = client(req)
    rospy.loginfo(res)
except rospy.ServiceException as e:
    rospy.logerr("Service didnot process your request:" + str(e))
