#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 22:15:55 2019

@author: abhijithneilabraham
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:27:24 2019

@author: abhijithneilabraham
"""

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
im='hari.jpeg'
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
#print(label)
CONV_SAMPLES = {
    'greetings' : ['Hi', 'hello', 'How are you', 'hey there', 'hey'],
    'taxi'      : ['book a '+str(label), 'need a ride', 'find me a'+str(label)],
    'datetime'  : ['what day is today', 'todays date', 'what time is it now',
                   'time now', 'what is the time']}
CLF = Classifier()
for key in CONV_SAMPLES:
    CLF.fit(CONV_SAMPLES[key], key)
X_TAXI = ['Go ' +str(label)+' to kochi ', 'need ' +str(label)+ 'to delhi', 'find me a '+str(label)+' for manhattan',
          'call a'+str(label)+' to calicut']
Y_TAXI = [{'service': str(label), 'destination': 'kochi'}, {'service': str(label), 'destination' : 'delhi'},
          {'service': str(label), 'destination' : 'manhattan'},
          {'service': str(label), 'destination' : 'calicut'}]

EX_TAXI = EntityExtractor()
EX_TAXI.fit(X_TAXI, Y_TAXI)



X_GREETING = ['Hii', 'helllo', 'Howdy', 'hey there', 'hey', 'Hi']
Y_GREETING = [{'greet': 'Hii'}, {'greet': 'helllo'}, {'greet': 'Howdy'},
              {'greet': 'hey'}, {'greet': 'hey'}, {'greet': 'Hi'}]

EX_GREETING = EntityExtractor()
EX_GREETING.fit(X_GREETING, Y_GREETING)


X_DATETIME = ['what day is today', 'date today', 'what time is it now', 'time now']
Y_DATETIME = [{'intent' : 'day', 'target': 'today'}, {'intent' : 'date', 'target': 'today'},
              {'intent' : 'time', 'target': 'now'}, {'intent' : 'time', 'target': 'now'}]

EX_DATETIME = EntityExtractor()
EX_DATETIME.fit(X_DATETIME, Y_DATETIME)
_EXTRACTORS = {'taxi':EX_TAXI,
               'greetings':EX_GREETING,
               'datetime':EX_DATETIME}
def get_response(u_query):
    '''
    Accepts user query and returns a response based on the class of query
    '''
    responses = {}
    rd_i = random.randint(0, 2)

    # Predict the class of the query.
    q_class = CLF.predict(u_query)

    # Run entity extractor of the predicted class on the query.
    q_entities = _EXTRACTORS[q_class].predict(u_query)
    if q_class == 'taxi':
        responses['taxi'] = 'Booking a '+q_entities['service']+ ' for '+q_entities['destination']

        def get_taxi():
            # Uber/Ola api.
            pass

    if q_class == 'datetime':
        responses['datetime'] = 'Today is '+str(datetime.datetime.today()).split(' ')[0]

        def get_dateime():
            # Calender api.
            pass

    if q_class == 'greetings':
        responses['greetings'] = ['Hey', 'Hi there',
                                  'Hello'][rd_i]+['\n        what would you like me to do ?', '',
                                                  '\n        what would you like me to do ?'][rd_i]

    return 'Agent : '+responses[q_class]
if __name__ == '__main__':
    # Greeting user on startup.
    print(get_response('Hi'))

    while True:
        UQUERY = input('you   : ')
        if UQUERY == 'bye':
            break
        RESPONSE = get_response(UQUERY)
        print(RESPONSE)


#    draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

# display output image    
#cv2.imshow("object detection", image)
#
## wait until any key is pressed
#cv2.waitKey()
#    
# # save output image to disk
#cv2.imwrite("object-detection.jpg", image)
#
## release resources
#cv2.destroyAllWindows()