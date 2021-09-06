# import rospy
import main
# import cv2 as cv
import time
# import os
import matplotlib.pyplot as plt
import matplotlib.image as IMG

# camera = cv.VideoCapture(0)

# for i in range(0, 10):
#     return_val, image = camera.read()
#     cv.imwrite(str(i) + ".jpg", image)
#     time_s = time.time()
#     objs, locs = main.obj_detect(main.model, str(i)+".jpg")
#     time_e = time.time()
#     print("detection is finished with {} sec.".format(time_e - time_s))
#     print(objs)
#     print('\n')
#     print(locs)
#     os.remove(str(i)+".jpg")
#     os.remove(str(i)+"_modified_.jpeg")
#
# del camera

# following code to be modified to use with ros
# Using ros service or ros messages publish a image and save it in same folder as the script with "detect.jpg" name

print("detection started")
s_t = time.time()
objs, locs, detection_score = main.obj_detect(main.model, "detect_image.jpg", acceptable_prob=0.2)
e_t = time.time()
print("totel time for detection: {}s".format(e_t-s_t))
img = IMG.imread("detect_image.jpg")
plt.imshow(img)
# time.sleep(60)

for i in range(0, len(objs)):
    print("Object:", objs[i], " location:", locs[i], " detection score:", detection_score[i])
    plt.scatter(locs[i][1], locs[i][0], color='b')

plt.show()
time.sleep(10)
plt.close('all')
# print(objs)
# print(locs)
# print(detection_score)

# Line above is main code for detection
# you can publish objs and locs using ros services or messages to use it as required

