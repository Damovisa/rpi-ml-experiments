import tensorflow as tf
import os
from time import sleep
from PIL import Image
import numpy as np
from picamera import PiCamera
from sense_hat import SenseHat

### Vars:

cam = PiCamera()
hat = SenseHat()
modelfile = './model-2/model.pb'
labelfile = './model-2/labels.txt'
tempimagefile = './pic.jpg'
G = [0, 200, 0]
Y = [200, 200, 0]
B = [0, 0, 200]
O = [0, 0, 0]
S = [200, 200, 200]
R = [200, 0, 0]
G = [0, 255, 0],
W = [255, 255, 255]
wait =   [O,O,S,S,S,S,O,O,
          O,O,S,O,O,S,O,O,
          O,O,S,O,O,S,O,O,
          O,O,O,S,S,O,O,O,
          O,O,O,S,S,O,O,O,
          O,O,S,O,O,S,O,O,
          O,O,S,Y,Y,S,O,O,
          O,O,S,S,S,S,O,O]

lego =   [O,O,O,Y,Y,O,O,O,
          O,Y,Y,Y,Y,Y,Y,O,
          Y,Y,O,Y,Y,O,Y,Y,
          Y,Y,Y,Y,Y,Y,Y,Y,
          Y,O,Y,Y,Y,Y,O,Y,
          Y,Y,O,O,O,O,Y,Y,
          O,Y,Y,Y,Y,Y,Y,O,
          O,O,O,W,W,O,O,O]

lock =   [O,O,O,S,S,O,O,O,
          O,O,S,O,O,S,O,O,
          O,O,S,O,O,S,O,O,
          O,G,G,G,G,G,G,O,
          O,G,G,G,G,S,G,O,
          O,G,G,G,G,S,G,O,
          O,G,G,G,G,S,G,O,
          O,G,G,G,G,G,G,O]

both =   [O,O,O,Y,Y,O,O,O,
          O,O,Y,Y,Y,Y,O,O,
          O,B,B,B,B,B,Y,O,
          Y,B,B,B,B,B,S,Y,
          Y,B,B,B,B,B,S,Y,
          O,B,B,B,B,B,Y,O,
          O,O,Y,Y,Y,Y,O,O,
          O,O,O,Y,Y,O,O,O]

nope =   [O,O,R,R,R,R,O,O,
          O,R,O,O,O,O,R,O,
          R,O,R,O,O,O,O,R,
          R,O,O,R,O,O,O,R,
          R,O,O,O,R,O,O,R,
          R,O,O,O,O,R,O,R,
          O,R,O,O,O,O,R,O,
          O,O,R,R,R,R,O,O]


### Functions:

def convert_to_imgarray(image):
    # RGB -> BGR conversion is performed as well.
    r,g,b = np.array(image).T
    imgarray = np.array([b,g,r]).transpose()
    return imgarray

def get_prediction(image_arr):
    ### Run TF prediction

    output_layer = 'loss:0'
    input_node = 'Placeholder:0'
    tags = []

    with tf.Session() as sess:
        prob_tensor = sess.graph.get_tensor_by_name(output_layer)
        predictions, = sess.run(prob_tensor, {input_node: [image_arr] })

        # Print out all of the results mapping labels to probabilities,
        #  and tag those above 0.5
        label_index = 0
        for p in predictions:
            truncated_probability = np.float64(round(p,4))
            print (labels[label_index], truncated_probability)
            if truncated_probability > 0.5:
                tags.append(labels[label_index])
            label_index += 1
    return tags

# Loading
hat.set_pixels(wait)

### Load Tensorflow Model

graph_def = tf.GraphDef()
labels = []

# import graph
with tf.gfile.FastGFile(modelfile, 'rb') as f:
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

# Get list of labels
with open(labelfile, 'rt') as lf:
    for l in lf:
        labels.append(l.strip())


### Get Images
        
#cam.preview_alpha = 128
cam.resolution = [227,227]
cam.start_preview()
sleep(2)
hat.clear()
# Loop, capturing images until a keypress

running = True
while running:
    event = hat.stick.wait_for_event()
    if event.action == "pressed":
        if event.direction == "middle":
            cam.capture(tempimagefile)
            image = Image.open(tempimagefile)
            image = convert_to_imgarray(image)
            prediction = get_prediction(image)
            if 'lego' in prediction and 'lock' in prediction:
                hat.set_pixels(both)
            elif 'lego' in prediction:
                hat.set_pixels(lego)
            elif 'lock' in prediction:
                hat.set_pixels(lock)
            else:
                hat.set_pixels(nope)
            sleep(2)
        if event.direction == "left":
            running = False
        hat.clear()
    sleep(0.1)
    
cam.stop_preview()
