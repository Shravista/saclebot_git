cmake_minimum_required(VERSION 2.8.3)

project(saclebot_description)

find_package(catkin REQUIRED COMPONENTS
            rospy     
            std_msgs
            message_generation)

add_service_files(
   FILES
   SacleBotState.srv
 )

generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
)

catkin_package(
  CATKIN_DEPENDS rospy
)

find_package(roslaunch)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
