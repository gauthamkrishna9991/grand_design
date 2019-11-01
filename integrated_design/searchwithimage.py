#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 23:34:42 2019

@author: abhijithneilabraham
"""

import random
from eywa.nlu import Classifier
from eywa.nlu import EntityExtractor

import cv2
import numpy as np
from eywa.nlu import Classifier
from eywa.nlu import EntityExtractor
import random
import datetime

# handle command line arguments
#ap = argparse.ArgumentParser()
#ap.add_argument('-i', '--image', required=True,
#                help = 'path to input image')
#ap.add_argument('-c', '--config', required=True,
#                help = 'path to yolo config file')
#ap.add_argument('-w', '--weights', required=True,
#                help = 'path to yolo pre-trained weights')
#ap.add_argument('-cl', '--classes', required=True,
#                help = 'path to text file containing class names')
#args = ap.parse_args()
im='test.jpg'
weights='yolov3.weights'
classes='yolov3.txt'
config='yolov3.cfg'
image = cv2.imread(im)

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

# read class names from text file

with open(classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# generate different colors for different classes 
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# read pre-trained model and config file
net = cv2.dnn.readNet(weights, config)

# create input blob 
blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

# set input blob for the network
net.setInput(blob)
def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
outs = net.forward(get_output_layers(net))

# initialization
class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4

# for each detetion from each output layer 
# get the confidence, class id, bounding box params
# and ignore weak detections (confidence < 0.5)
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

# go through the detections remaining
# after nms and draw bounding box
for i in indices:
    i = i[0]
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    label = str(classes[class_ids[i]])
print(label)
CONV_SAMPLES = {
    'car'       : [ "test drive this <img> ", " cost of this <img> vehicle", "what is the mileage of this <img> vehicle",
                    "which model vehicle is this <img>" ],
    'gender'    : [ " <img> What is  the disease associated with this  gender", " Diseases <img> these gender have", "Find out the gender problems of <img> Abhijith"],
    'number' : ['how many people in this <img> ', 'number of people in <img> ', ' <img>count the people']
}
CLF = Classifier()
for key in CONV_SAMPLES:
    CLF.fit(CONV_SAMPLES[key], key)
u_query="diseases this gender have <img>"
q_class = CLF.predict(u_query)
print(q_class)


from pathlib import Path
import cv2
import dlib
import numpy as np
from contextlib import contextmanager
from wide_resnet import WideResNet

def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=0.8, thickness=1):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)


@contextmanager
def video_capture(*args, **kwargs):
    cap = cv2.VideoCapture(*args, **kwargs)
    try:
        yield cap
    finally:
        cap.release()


def yield_images():
    # capture video
    with video_capture(0) as cap:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            # get video frame
            ret, img = cap.read()

            if not ret:
                raise RuntimeError("Failed to capture image")

            yield img


def yield_images_from_dir(image_dir):
    image_dir = Path(image_dir)

    for image_path in image_dir.glob("*.*"):
        img = cv2.imread(str(image_path), 1)

        if img is not None:
            h, w, _ = img.shape
            r = 640 / max(w, h)
            yield cv2.resize(img, (int(w * r), int(h * r)))



#    args = get_args()
depth = 16
k = 8
weight_file = 'agegender.hdf5'
margin = 0.4
img = cv2.imread('neilan.jpg')


# for face detection
detector = dlib.get_frontal_face_detector()

# load model and weights
img_size = 64
model = WideResNet(img_size, depth=depth, k=k)()
model.load_weights(weight_file)


input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_h, img_w, _ = np.shape(input_img)

# detect faces using dlib detector
detected = detector(input_img, 1)
faces = np.empty((len(detected), img_size, img_size, 3))
label_list=[]

if len(detected) > 0:
    for i, d in enumerate(detected):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
        xw1 = max(int(x1 - margin * w), 0)
        yw1 = max(int(y1 - margin * h), 0)
        xw2 = min(int(x2 + margin * w), img_w - 1)
        yw2 = min(int(y2 + margin * h), img_h - 1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
        faces[i, :, :, :] = cv2.resize(img[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))

    # predict ages and genders of the detected faces
    results = model.predict(faces)
    predicted_genders = results[0]
    ages = np.arange(0, 101).reshape(101, 1)
    predicted_ages = results[1].dot(ages).flatten()
    

    # draw results
    for i, d in enumerate(detected):
        label = "{}, {}".format(int(predicted_ages[i]),
                                "M" if predicted_genders[i][0] < 0.5 else "F")
        label_list.append(label)
#            draw_label(img, (d.left(), d.top()), label)

#        cv2.imwrite("result.jpg", img)
    #label=[label]
    print(label_list)
if q_class=='gender':
    print(label_list[i][4:])



