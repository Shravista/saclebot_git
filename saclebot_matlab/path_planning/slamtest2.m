bag=rosbag('test_2021-08-31-21-23-45.bag');
scan=readMessages(bag);
Minscanrange=scan{1}.RangeMin;
maxLidarRange=scan{1}.RangeMax;
Angles=linspace(scan{1}.AngleMin,scan{1}.AngleMax,720);
messagelength=length(scan);
Scan=cell(messagelength,1);

for i=1:messagelength
    Scan{i}=lidarScan(scan{i}.Ranges,Angles);
end

mapResolution = 100;
slamAlg = lidarSLAM(mapResolution, maxLidarRange);
slamAlg.LoopClosureThreshold = 210;  
slamAlg.LoopClosureSearchRadius = 8;

for i=1:5
    [isScanAccepted, loopClosureInfo, optimizationInfo] = addScan(slamAlg, Scan{i});
    if isScanAccepted
        fprintf('Added scan %d \n', i);
    end
end
figure;
show(slamAlg);
title({'Map of the Environment','Pose Graph for Initial 10 Scans'});
firstTimeLCDetected = false;

figure;
for i=5:length(Scan)
    [isScanAccepted, loopClosureInfo, optimizationInfo] = addScan(slamAlg, Scan{i});
    if ~isScanAccepted
        continue;
    end
    % visualize the first detected loop closure, if you want to see the
    % complete map building process, remove the if condition below
    if optimizationInfo.IsPerformed && ~firstTimeLCDetected
        show(slamAlg, 'Poses', 'off');
        hold on;
        show(slamAlg.PoseGraph); 
        hold off;
        firstTimeLCDetected = true;
        drawnow
    end
end
title('First loop closure');
figure
show(slamAlg);
title({'Final Built Map of the Environment', 'Trajectory of the Robot'});
[Scan, optimizedPoses]  = scansAndPoses(slamAlg);
map = buildMap(Scan, optimizedPoses, mapResolution, maxLidarRange);
figure; 
show(map);
hold on
show(slamAlg.PoseGraph, 'IDs', 'off');
hold off
title('Occupancy Grid Map Built Using Lidar SLAM');