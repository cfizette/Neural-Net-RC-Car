import threading
import io
import socket
import struct
import serial

import cv2
import numpy as np
import os
import time
from keras.models import load_model
from keras.models import Sequential

# Com port for Arduino
com_port = 3

# IP Address
ip_address = '192.168.1.14'


def drive_car():
    class Driver(object):

        def __init__(self):
            self.server_socket = socket.socket()
            self.server_socket.bind((ip_address, 8000))
            self.server_socket.listen(0)
            self.connection = self.server_socket.accept()[0].makefile('rb')
            self.model = load_model('test_model_2.h5')
            self.ser = serial.Serial(com_port, 115200, timeout=1)
            self.send_inst = True
            self.drive()


        def drive(self):

            try:
                stream_bytes = ' '

                while self.send_inst:
                    # Read the length of image, if 0 break
                    image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break
                    
                    # Construct stream and read image from connection
                    image_stream = io.BytesIO()
                    image_stream.write(self.connection.read(image_len))                 
                    data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
                    image = cv2.imdecode(data, 0)
                    
                    # Crop Image
                    image = image[120:, :]
                  
                    # Run image through NN
                    image_formatted = np.resize(image, (120, 320, 1))
                    image_formatted = np.expand_dims(image_formatted, axis=0)
                    pred = self.model.predict(image_formatted/255, 1).round()
     
               
                    # Perform action based off predection
                    print(pred[0,:])
                    if pred[0,0] == 1:
                        print('Forward Left')
                        self.ser.write(b'6')
                    elif pred[0,1] == 1:
                        print('Forward Right')
                        self.ser.write(b'5')
                    elif pred[0,2] == 1:
                        print("Forward")
                        self.ser.write(b'1')
                                              
                    # Show video feed                     
                    try:
                        cv2.imshow('image', image)
                        cv2.waitKey(1)
                    except:
                        print("error displaying image")
                        
            except IOError as e:
                print(e)

    Driver()
    
drive_car()























