#!/bin/bash


set -e

ECHO_PREFIX="[saclebot_ws_setup.sh]"
#export ROS_MASTER_URI=http://saclebot:11311
echo "$ECHO_PREFIX" "set ROS master: " "$ROS_MASTER_URI"


ROS=/opt/ros/noetic/setup.bash
source "$ROS"
echo "$ECHO_PREFIX" "sourced ROS installation:" "$ROS"
workspace=/sacle_bot
source "$workspace"/devel/setup.bash
echo "$ECHO_PREFIX" "sourced workspace:" "$workspace"

echo "$ECHO_PREFIX" "execute" "$@"
exec "$@"

#export ROS_HOSTNAME=$(hostname --ip-address)
#source "/opt/ros/$ROS_DISTRO/setup.bash"
#roslaunch saclebot_bringup saclebot_bringup.launch
