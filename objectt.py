import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import matplotlib
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import cv2
import urllib
import urllib.request
import time
import os
import tkinter as tk
from tkinter import ttk
import abcdabcd
from datetime import datetime
import predict
import bagofwords1
import subprocess
import pytesseract

from utils import label_map_util

from utils import visualization_utils as vis_util

#######################################################################################################################################################################
def main(url,readfile,writefile): 
  sys.path.append("..")


  MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
  MODEL_FILE = MODEL_NAME + '.tar.gz'
  DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

  # Path to frozen detection graph. This is the actual model that is used for the object detection.
  PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

  # List of the strings that is used to add correct label for each box.
  PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

  NUM_CLASSES = 90
  # ## Load a (frozen) Tensorflow model into memory.

  # In[ ]:
#  global detection_graph,category_index
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')


  # ## Loading label map
  # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

  # In[ ]:

  label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
  categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
  category_index = label_map_util.create_category_index(categories)


  while True:
    if(os.stat(readfile).st_size != 0):
        f = open(readfile,'r+')
        f2=f.read()
        f.truncate(0)
        f.close()
        print(f2)
        if(f2=="Shutdown" or f2=="shut down" or f2=="shutdown" or f2=="bye"):
          break
        word_list = f2.split()
        mm=word_list[-1]
        option=bagofwords1.select_option(f2)
        #option=abcdabcd.select_option(f2)
        print(option)
        operation(option,mm,url,readfile,writefile,detection_graph,category_index)
                
##################################################################################################################################################################################
def popupmsg(msg,url):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=("Helvetica", 100))
    popup.configure(bg='red')
    label.pack(side="top", fill="x", padx=100, pady=100)
    B1 = ttk.Button(popup, text="Show", command =show_entry_fields(url) )
    B1.pack()
    B2 = ttk.Button(popup, text="Quit", command =show_entry_fields1(popup) )
    B2.pack()
    popup.mainloop()

def show_entry_fields(k):
    return lambda : show(k)

def show_entry_fields1(k1):
    return lambda : destroy(k1)

def destroy(popup):
    popup.destroy()
    if 'proc' in globals():
        proc.kill()

def show(url):
    global proc
    proc = subprocess.Popen([sys.executable, "ipwebcam.py"],stdin=subprocess.PIPE)
    proc.stdin.write(url.encode())
    proc.stdin.close()
    
def operation(option,mm,url,readfile,writefile,detection_graph,category_index):
    if (option=="Follow"):
        object2(mm,url,readfile,writefile,detection_graph,category_index)        
    elif (option=="Search"):
        object1(mm,url,readfile,writefile,detection_graph,category_index)
    elif (option=="Date Time"):
        zz=str(time.ctime())
        abc1,abc2,abc3,abc4,abc5=zz.split(" ")
        abcd1,abcd2,_ = abc4.split(":")
        zzz = "Date Time;"+abc2+";"+abc3+";"+abcd1+";"+abcd2
        print(zz)
        f = open(writefile,'w')
        f.write(zzz)
        f.close()
    elif (option=="Need help"):
        f = open(writefile,'w')
        f.write("Close;Need Help")
        f.close()
        popupmsg("NEED HELP",url)
    elif (option=="Read"):
        f = open(writefile,'w')
        f.write("Close;Read")
        f.close()
        text_detect(url)

    elif(option=="Currency"):
        f = open(writefile,'w')
        f.write("Close;Currency")
        f.close()
        
        zz=url+" "+writefile
        zz=predict.detect_currency(url)
        zz=str(zz)
        f = open(writefile,'w')
        f.write("Currency;"+zz+";0;0")
        f.close()
    elif(option=="Overview"):
        object3(mm,url,readfile,writefile,detection_graph,category_index)    

######################################################################################################################################################################################
def object1(mm,url,readfile,writefile,detection_graph,category_index):
    #container = av.open(url)
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
        while True:
            with urllib.request.urlopen(url) as imgResp:
              imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
              image_np=cv2.imdecode(imgNp,-1)    
                #ret, image_np = cap.read()
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
              image_np_expanded = np.expand_dims(image_np, axis=0)
              image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
              boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
              scores = detection_graph.get_tensor_by_name('detection_scores:0')
              classes = detection_graph.get_tensor_by_name('detection_classes:0')
              num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                # Actual detection.
              (boxes, scores, classes, num_detections) = sess.run(
                  [boxes, scores, classes, num_detections],
                  feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
              vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    mm,
                    readfile,
                    writefile,
                    use_normalized_coordinates=True,
                    line_thickness=8)
              if(os.stat(readfile).st_size != 0):
                f = open(readfile,'r+')
                a1=f.read()
                f.truncate(0)
                f.close()
                mm = str(a1)
                word_list = mm.split()
                mm=word_list[-1]
                print(a1)
              if( mm == "CLOSE" or mm == "close" or mm=="Close"):
                cv2.destroyAllWindows()
                f = open(writefile,'w')
                f.write("Close;Search")
                f.close()                
                break

              cv2.imshow('object detection',cv2.resize(image_np,(800,600)))
              if cv2.waitKey(1) & 0xFF==ord('q'):
                cv2.destroyAllWindows()
                break

######################################################################################################################################################################
def object2(mm,url,readfile,writefile,detection_graph,category_index):
    count=0
    center_position=0
  #container = av.open(url)

    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:

          while True:
                with urllib.request.urlopen(url) as imgResp:
                  imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
                  image_np=cv2.imdecode(imgNp,-1) 
                  

                  #if(count1==1):
                    #if(xmin1>30 and xmax1<610 and ymin1>30 and ymax1<450):
                      #image_np= image_np[int(ymin1) - 25:int(ymin1) + int(ymax1)+ 25,int(xmin1) - 25:int(xmin1) + int(xmax1) + 25]
                    #NOTE: its img[y: y + h, x: x + w] 


                    #ret, image_np = cap.read()
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                  image_np_expanded = np.expand_dims(image_np, axis=0)
                  image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                  boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                  scores = detection_graph.get_tensor_by_name('detection_scores:0')
                  classes = detection_graph.get_tensor_by_name('detection_classes:0')
                  num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                  (boxes, scores, classes, num_detections) = sess.run(
                      [boxes, scores, classes, num_detections],
                      feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                  count,center_position=vis_util.visualize_boxes_and_labels_on_image_array1(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        mm,
                        readfile,
                        writefile,
                        count,
                        center_position,
                        use_normalized_coordinates=True,
                        line_thickness=8)
                  if(os.stat(readfile).st_size != 0):
                    f = open(readfile,'r+')
                    a1=f.read()
                    f.truncate(0)
                    f.close()
                    mm = str(a1)
                    word_list = mm.split()
                    mm=word_list[-1]
                    print(a1)
                  if( mm == "CLOSE" or mm == "close" or mm=="Close" or mm=="stop"):
                    cv2.destroyAllWindows()
                    f = open(writefile,'w')
                    f.write("Close;Follow")
                    f.close()
                    break

                  cv2.imshow('object detection',cv2.resize(image_np,(800,600)))
                  if cv2.waitKey(1) & 0xFF==ord('q'):
                    cv2.destroyAllWindows()
                    break
#############################################################################################################################################################################
def object3(mm,url,readfile,writefile,detection_graph,category_index):
    #container = av.open(url)
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
            while True:
                with urllib.request.urlopen(url) as imgResp:
                  imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
                  image_np=cv2.imdecode(imgNp,-1)    
                    #ret, image_np = cap.read()
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                  image_np_expanded = np.expand_dims(image_np, axis=0)
                  image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                  boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                  scores = detection_graph.get_tensor_by_name('detection_scores:0')
                  classes = detection_graph.get_tensor_by_name('detection_classes:0')
                  num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    # Actual detection.
                  (boxes, scores, classes, num_detections) = sess.run(
                      [boxes, scores, classes, num_detections],
                      feed_dict={image_tensor: image_np_expanded})
                    # Visualization of the results of a detection.
                  vis_util.visualize_boxes_and_labels_on_image_array3(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        readfile,
                        writefile,
                        use_normalized_coordinates=True,
                        line_thickness=8)
                  if(os.stat(readfile).st_size != 0):
                    f = open(readfile,'r+')
                    a1=f.read()
                    f.truncate(0)
                    f.close()
                    mm = str(a1)
                    word_list = mm.split()
                    mm=word_list[-1]                    
                    print(a1)
                  if( mm == "CLOSE" or mm == "close" or mm=="Close"):
                    cv2.destroyAllWindows()
                    f = open(writefile,'w')
                    f.write("Close;Overview")
                    f.close()                    
                    break

                  cv2.imshow('object detection',cv2.resize(image_np,(800,600)))
                  if cv2.waitKey(1) & 0xFF==ord('q'):
                    cv2.destroyAllWindows()
                    break
#############################################################################################################################################################################

          
def text_detect(url):
  i=0
  while True:
    with urllib.request.urlopen(url) as imgResp:
      imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
      image_np=cv2.imdecode(imgNp,-1)        
      i=i+1
      if(i==5):
        break
  ####write ur code here




  # Convert to gray
  img = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale
  _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
  kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
  dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
  _, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

  # for each contour found, draw a rectangle around it on original image
  i=1
  for contour in contours:
      # get rectangle bounding contour
      [x,y,w,h] = cv2.boundingRect(contour)
      
      # discard areas that are too large
      if h>300 and w>300 or h<40 or w<40:
          continue


      # draw rectangle around contour on original image
      cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
      crop_img = image[y-5: y + h+5,x-5: x + w+5]
      aa(crop_img)
      cv2.imwrite("cropped"+str(i)+".png", crop_img)
      i=i+1



def aa(img):
    #img = cv2.imread(image)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    a = img

    #  Apply threshold to get image with only black and white
    _,img = cv2.threshold(img,150,255,cv2.THRESH_BINARY_INV) # threshold
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    b = img

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(b)
    if(result !=""): 
      f = open(writefile,'w')
      f.write("Read;"+zz)
      f.close()    
    #print(result.encode("utf-8"))
    print(result)
      
#############################################################################################################################################################################
r=str(sys.stdin.read())
print(r)
ab1,ab2,ab3,ab4=r.split(".")
#url='http://192.168.0.2'
#ab1,ab2,ab3,ab4=url.split(".")
url="http://"+r+":8080/shot.jpg"
print(url)
readfile = ab4 + "_read.txt"
writefile = ab4 + "_write.txt"

main(url,readfile,writefile)

time.sleep(10)
os.remove(readfile)
os.remove(writefile)
