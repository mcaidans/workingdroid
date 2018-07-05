import socket
import videofeed as vf
import serial
import time

train = 0

milli_time = lambda: int(round(time.time() * 1000))

folder_loc = "/home/pi/Desktop/training_data"
training_name = str(milli_time()) + str(".csv")

ip = "192.168.43.7"
post = 9006

ser = serial.Serial('/dev/ttyACM0', 9600)


while True:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((ip, post))
    print("Listening for connection on\nip: {}\nport: {}".format(ip, post))
    serversocket.listen(1)
    connection, address = serversocket.accept()
    print("Connected!")
    count = 4
    throttle = 0
    while True:
        
        buf = connection.recv(100000).decode()
        
        if buf:
            #start = time.time()
            #buffDecode = time.time() - start
            commands = buf[buf.rfind('(') + 1:buf.rfind(')')]
            angle, throttle, train_flag, quit_flag = commands.split(',')
            print(angle, throttle, train_flag, quit_flag)
            #time.sleep(0.1)
            #newThrottle = 0
            #ser.write(str.encode(str(angle) + ", " + str(newThrottle)))
            
            if int(quit_flag):
                print("Ending loop")
                break
            train = train_flag
            #buffDecode2 = time.time() - start
            if int(train):
                print("Save image")
                image_name = str(milli_time())
                vf.add_training_data(image_name, ".png", str(angle), str(throttle))
                print("Save Done")
            #saveTrain = time.time() - start
            ser.write(str.encode(str(angle) + ", " + str(throttle)))
            #ard = time.time() - start
            #print("BuffDecode:%f\nBuffSeperate:%f\nTrainSave:%f\nArduino:%f" % (buffDecode, buffDecode2, saveTrain, ard))
##        if throttle == 100:
##            if count == 4:
##                throttle = 100
##                count = 0
##                print("hit")
##            else:
##                throttle = 0
##                count += 1
        #time.sleep(.05)
        
    print("Saving training data")
    serversocket.shutdown(socket.SHUT_RDWR)
    serversocket.close()
    vf.save_training_data(folder_loc, training_name)
    print("Training data saved.")