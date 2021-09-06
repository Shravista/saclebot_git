clear;
clc;
origin = [0; 0; 0; 1];
endPosEndEffector = [1, 1, 1];
%midPos = zeros(4,3);
robot = importrobot("./../saclebot_description/urdf/saclebot_description.urdf");
initialJointCongfig = robot.homeConfiguration;
startTform = getTransform(robot, initialJointCongfig, 'gripper_base_link', 'base_link');
%startPosEndEffector  = Transform * origin;
endTform = trvec2tform(endPosEndEffector);
ik = inverseKinematics('RigidBodyTree', robot);
[tforms, vel, acc] = transformtraj(startTform, endTform, [0,1], 0:0.1:1);			%tforms - all joint actutaion array
show(robot, initialJointCongfig);
w = [.25,.25,.25,1,1,1];
for k = 1:11
    [Interconfig, ~] = ik('gripper_base_link', tforms(:,:,k), w, initialJointCongfig);
    initialJointCongfig = Interconfig;
    show(robot, Interconfig);
end