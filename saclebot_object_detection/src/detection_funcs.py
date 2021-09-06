import tensorflow as tf
#tf.get_logger().setLevel('INFO')

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
# from PIL import ImageColor
# from PIL import ImageDraw
# from PIL import ImageFont
from PIL import ImageOps

import time
# import cv2 as cv
# import os

########################################################################################################################
#Download model from: https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1
########################################################################################################################
t_S = time.time()
model = tf.saved_model.load("").signatures['default']
t_f = time.time()
print("model loaded in {} sec.".format(t_f-t_S))


def display_image(image) -> np.array:
    """ Function to display image using matplot lib

    :param image: image to be displayed
    :return: nothing
    """

    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)


# resize_image(url, new_width=256, new_height=256, display=False) returns file name of modified image
def resize_image(url, new_width=256, new_height=256, display=False) -> [str, int, int, bool]:
    """Function to resize image to required dimension

    :param url : url of image or path of image file
    :param new_width : required width of output image, default value: 256
    :param new_height : required height of output image, default value: 256
    :param display : To display print image ot not, default value: False
    :return:
    """
    # _, filename = tempfile.mkstemp(suffix=".jpg")
    filename = url[0] + "_modified_" + ".jpeg"
    # response = urlopen(url)
    # image_data = response.read()
    # image_data = BytesIO(image_data)
    pil_image = Image.open(url)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
        display_image(pil_image)
    return filename


def load_img(path) -> str:
    """ function to load image

    :param path : path to image
    :return: image as tf tensor
    """
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img


# image_ready(path) returns image in tensorflow numpy array ready to feed to the network

def image_ready(path) -> str:
    """Returns image in tensorflow numpy array ready to feed to the network
    
    :param path: Path of image
    :return: image in tf numpy array
    """
    image = resize_image(path)
    img = tf.io.read_file(image)
    img = tf.image.decode_jpeg(img, channels=3)
    return tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]


def location_box(box_coordi, image) -> [list, np.array]:
    """Function to locate center of enclosing box of the object

    :param box_coordi : coordinates of box enclosing detected object
    :param image: image
    :return: position of center of box in image
    """
    im_width, im_hight, im_depth = load_img(image).shape
    h_scale = 256/im_hight
    w_scale = 256/im_width
    # print(image.shape)
    position = np.array(
        [(box_coordi[0] + box_coordi[2]) * 0.5 * im_width, (box_coordi[1] + box_coordi[3]) * 0.5 * im_hight])
    return position


def obj_label_position(result, acceptable_prob, image) -> [tuple, float, np.array]:
    """

    :param result: result of the detection through image
    :param acceptable_prob: thresholding probability of object detection
    :param image: image
    :return: object labels and its positions
    """
    labels = result['detection_class_entities']
    box_positions = result['detection_boxes']
#    print(box_positions)
    labels_detection_score = result['detection_scores']

    idx = [i for i in range(0, len(labels_detection_score)) if labels_detection_score[i] >= acceptable_prob]
    obj_labes = np.array([labels[i] for i in idx])
    obj_box_limit = np.array([box_positions[i] for i in idx])
    obj_position = np.array([location_box(obj_box_limit[i], image) for i in idx])
    detectoin_score = np.array([labels_detection_score[i] for i in idx])
    # print(obj_position)

    return obj_labes, obj_position, detectoin_score


"""
obj_detect(detector, image, acceptable_prob=0.75) returns tuple of nx2 dimension where n is no of detected objects 
having probability > acceptable prob first element of tuple is numpy array of labels of detected objects and second 
element is numpy array of center of bounding boxes of the objects    
"""


def obj_detect(detector, image, acceptable_prob=0.6) -> [tf.saved_model, str, float]:
    """

    :param detector: object detector
    :param image: path image in which objects are to be detected
    :param acceptable_prob: thresholding probability, <1 and >0 always
    :return: objects and location of the objects in image
    """
    img = image_ready(image)
    result = detector(img)
    objs, locs, detection_score = obj_label_position(result, acceptable_prob, image)
    return objs, locs, detection_score

########################################################################################################################

if __name__ == "__main__":
    objs, locs, detection_scores = obj_detect(model, "detect_image.jpg")
    print(f"Objects :\n{objs}")
    print(f"Locations : \n {locs}")
    print(f"Detection: \n {detection_scores}")

