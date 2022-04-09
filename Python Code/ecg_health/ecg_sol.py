import numpy as np
import cv2
from  matplotlib import pyplot as plt
import pyrebase
import time
import os
import json
from tkinter import *
from tkinter import messagebox

firebaseConfig = {
  "apiKey": "AIzaSyBQWGbRvg04QMczG2895w1ZEzEKK-uT3kk",
  "authDomain": "ecgdata-e1079.firebaseapp.com",
  "databaseURL": "https://ecgdata-e1079-default-rtdb.firebaseio.com",
  "projectId": "ecgdata-e1079",
  "storageBucket": "ecgdata-e1079.appspot.com",
  "messagingSenderId": "561365440312",
  "appId": "1:561365440312:web:12162d1cd0dbf7ff5393cd"
}

firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
storage=firebase.storage()

#open the camera and record the video save the video in firebase .use that firebase video to draw the ecg graph
#save that graph again to firebase to upload in personal health details
root = Tk()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
cap.set(cv2.CAP_PROP_FPS, 30)
# Image crop
x, y, w, h = 800, 500, 100, 100
x, y, w, h = 950, 300, 100, 100
heartbeat_count = 128
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count
# Matplotlib graph surface
fig = plt.figure()
#setting the grid size to 1x1
ax = fig.add_subplot(111)
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # converting to RGB scale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    crop_img = img[y:y + h, x:x + w]
    # Update the data
    heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
    heartbeat_times = heartbeat_times[1:] + [time.time()]
    # Draw matplotlib graph to numpy array
    ax.plot(heartbeat_times, heartbeat_values)
    
    fig.canvas.draw()
    plot_img_np = np.frombuffer(fig.canvas.tostring_rgb(),dtype=np.uint8)#interprets buffer as 1-D array
    plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))#redefines the shape using an array
    plt.cla() #clears the current axis

    # Display the frames
    cv2.imshow('Crop', crop_img)
    cv2.imshow('Graph', plot_img_np)
    plt.savefig("s.png")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 


'''path_on_cloud="images/ss.jpg"
path_local="s.png"
storage.child(path_on_cloud).put(path_local)'''




cap.release()
cv2.destroyAllWindows()


