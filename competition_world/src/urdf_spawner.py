#! /usr/bin/env python3
import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from std_srvs.srv import Trigger, TriggerResponse
import rospkg
from urdf_parser_py.urdf import URDF
import numpy as np

class DynamicItemsLocation(object):
    def __init__(self):
        rospy.init_node("saclebot_objects_urdf_spawner")
        rospy.wait_for_service("/gazebo/spawn_urdf_model")
        rospy.wait_for_service("/gazebo/delete_model")
        
        self.urdfSpawnClient = rospy.ServiceProxy("/gazebo/spawn_urdf_model",SpawnModel)
        self.deleteModelClient = rospy.ServiceProxy("/gazebo/delete_model",DeleteModel)
        self.modelStateClient = rospy.ServiceProxy("/gazebo/get_model_state",GetModelState)
        self.relocate = rospy.Service("/saclebot/relocate_trash",Trigger, self.callback)
        
        rospack = rospkg.RosPack()
        self.package  = rospack.get_path("competition_world") + "/urdf/"
        self.urdfPaths = np.array(["coke_can.urdf","red_paper_cup.urdf","green_paper_cup.urdf"])
        self.response = TriggerResponse()
        rospy.on_shutdown(self.shutdownhook)
        
        self.spawnModelReq = SpawnModelRequest()
        self.delModelReq = DeleteModelRequest()
        
        self.ctrl_c = False
        self.modelNames = np.array(["coke_can","red_paper_cup","green_paper_cup"])
        
        rospy.loginfo("Service: /saclebot/relocate_trash started")
        
        # temp
        self.getModelReq = GetModelStateRequest()
        
        
    def shutdownhook(self):
        self.ctrl_c = True
        for modelName in self.modelNames:
            self.delModelReq.model_name = modelName         
            res = self.deleteModelClient(self.delModelReq)
            rospy.loginfo(res)
        rospy.loginfo("Shutting Down")
    
    def callback(self,req):
        rospy.loginfo("Responding to the spawning request")
        
        try:
            for path, modelName in zip (self.urdfPaths, self.modelNames):
                self.item = URDF.from_xml_file(self.package+path)
                self.xml_str = self.item.to_xml_string()
                pose = rospy.get_param("/saclebot_"+modelName+"_pose_config")
                
                self.spawnModelReq.model_name = modelName
                self.spawnModelReq.model_xml = self.xml_str
                self.spawnModelReq.initial_pose.position.x = pose["X"]
                self.spawnModelReq.initial_pose.position.y = pose["Y"]
                self.spawnModelReq.initial_pose.position.z = pose["Z"]
                
                self.getModelReq.model_name = modelName  
                self.delModelReq.model_name = modelName          
                modelState = self.modelStateClient(self.getModelReq)
                if modelState.success:
                    res = self.deleteModelClient(self.delModelReq)
                    rospy.loginfo(res)
                
                res = self.urdfSpawnClient(self.spawnModelReq)
                self.response.success = res.success
                self.response.message = res.status_message 
            
            rospy.loginfo(f"Spawn the models : {self.modelNames} is success")
            return self.response
        except Exception as e:
            rospy.logerr(e)

if __name__ == "__main__":
    
    i = DynamicItemsLocation()
    rospy.spin()
    


