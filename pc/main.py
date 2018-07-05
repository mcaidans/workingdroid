# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2
import socket

ip = "localhost"
post = 9006

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((ip, post))


FORWARD = 82
RIGHT = 83
LEFT = 81
BACK = 84
TRAIN = 116
QUIT = 113


forward = 0
angle = 75
send = False
train = 0
stop = 0

c = cv2.VideoCapture(0)
print(c.isOpened()) # False
print(c.read()) # (False, None)

while 1:

    key = cv2.waitKey(1)
    _, f = c.read()
    cv2.imshow("test", f)

    if key == FORWARD:
        print("Forward")
        forward = 100
        send = True
    if key == BACK:
        forward = 0
        send = True
    if key == LEFT:
        if angle < 130:
            angle += 30
        send = True
    if key == RIGHT:
        if angle > 20:
            angle -= 30
        send = True
    if key == TRAIN:
        send = True
        if train:
            train = 0
            print("Training Deactivated")
        else:
            train = 1
            print("Training Activated")

    if key == QUIT:
        stop = 1
        send = True

    if send:
        print(str.encode("(" + str(angle) + ", " + str(forward) + ", " + str(train) + ", " + str(stop) + ")"))
        clientsocket.send(str.encode("(" + str(angle) + ", " + str(forward) + ", " + str(train) + ", " + str(stop) + ")"))
        print("sent")

    send = False
    if stop:
        break
