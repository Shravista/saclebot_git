#! /usr/bin/env python3
import rospy
from saclebot_description.srv import SacleBotState, SacleBotStateResponse
from gazebo_msgs.srv import SetModelState, SetModelStateRequest
from scipy.spatial.transform import Rotation as TF
import numpy as np

class RelocateBot(object):
    def __init__(self):
        rospy.init_node("saclebot_relocate")
        rospy.wait_for_service("/gazebo/set_model_state")
        
        self.modelClient = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)
        self.relocate = rospy.Service("/saclebot/relocate_bot",SacleBotState,self.callback)
        
        self.modelName = "saclebot"
        self.res = SacleBotStateResponse()
        self.req = SetModelStateRequest()
        self.req.model_state.model_name = self.modelName
        
        rospy.on_shutdown(self.shutdownhook)
        self.ctrl_c = False
    
    def callback(self,msg):
        x = msg.x
        y = msg.y
        x = np.round(x,2)
        y = np.round(y,2)
        yaw = 0
        
        if (x>0.0 and y <= -0.8) or (x>0.0 and y>= 3.8) or (x >3.8 and y>=3.8) or (x >=3.8 and y<=-0.8):
            yaw = 3.1416
            
        elif (x>=3.8 and (y>0 and y<3.8)) or (y>0 and x<=-0.8):
            yaw = -1.5708
            
        elif (y<=-0.8 and x <= -0.8):
            yaw = 1.5708
        else:
            rospy.logerr("Wrong request!!!")
        
        
        euler = TF.from_euler('zyx',[yaw,0,0])
        quat = euler.as_quat()
        
        self.req.model_state.pose.position.x = x
        self.req.model_state.pose.position.y = y
        self.req.model_state.pose.position.z = 0.10
        
        self.req.model_state.pose.orientation.x = quat[0]
        self.req.model_state.pose.orientation.y = quat[1]
        self.req.model_state.pose.orientation.z = quat[2]
        self.req.model_state.pose.orientation.w = quat[3]
        
        res = self.modelClient(self.req)
        
        if res.success:
            self.res.success = True
            self.res.message = f"Your request is successfully processed for the given positions (x,y): {x,y}"
        
        else:
            self.res.success = False
            self.res.message = f"Your request is failed for the given positions (x,y): {x,y}"
        
        return self.res
    
    def shutdownhook(self):
        self.ctrl_c = True
        rospy.loginfo("Shutting Down")


if __name__ == "__main__":
    relocate = RelocateBot()
    rospy.spin()
