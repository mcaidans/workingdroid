import cv2
import numpy as np
import pandas as pd

c = cv2.VideoCapture(0)
c.set(3, 1280)
c.set(4, 720)

frame_names = []
frames = []
angles = []
throttles = []

def get_image():
    _, f = c.read()
    return f

def save_image(name, frame=None):
    if frame is None:
        frame = get_image()
    cv2.imwrite(name, frame)

def add_training_data(name, filetype, angle, throttle, frame=None):
    if frame is None:
        frame = get_image()
    frame_names.append(name + filetype)
    frames.append(frame)
    angles.append(angle)
    throttles.append(throttle)

def save_training_data(folder_loc, name):
    df = pd.DataFrame({"image": frame_names,
                       "angle": angles,
                       "throttle": throttles})
    df.to_csv(folder_loc + "/" + name, index=False)
    for i in range(len(frame_names)):
        save_image(folder_loc + "/" + frame_names[i], frames[i])

def show_image(name="droidcam", frame=None):
    if frame is None:
        frame = get_image()
    cv2.imshow(name, frame)
    
'''
while(1):
    #cv2.imwrite("output.png", f)
    if cv2.waitKey(5)==27:
        break
cv2.destroyAllWindows()
'''
