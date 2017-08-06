import threading
import io
import socket
import struct
import serial
import pygame
import _thread as thread
import cv2
import numpy as np
import os
import time


'''
Note that the pygame window will take a few moments to warm up and may be unresponsive during this time.
'''

folder = 'training_images'


def rc_controller():
    ser = serial.Serial(3, 115200, timeout=1)
    pygame.init()
    disp = pygame.display.set_mode((800, 600))
    print('getting input')
    # Get keyboard input and send data
    while True:


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                key_input = pygame.key.get_pressed()

                if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                    print('Forward Right')
                    ser.write(b'5')

                elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                    print('Forward Left')
                    ser.write(b'6')

                elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                    print('Reverse Left')
                    ser.write(b'8')

                elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                    print('Reverse Right')
                    ser.write(b'7')

                elif key_input[pygame.K_UP]:
                    print("Forward")
                    ser.write(b'1')

                elif key_input[pygame.K_DOWN]:
                    print("Reverse")
                    ser.write(b'2')

                elif key_input[pygame.K_RIGHT]:
                    print("Right")
                    ser.write(b'4')

                elif key_input[pygame.K_LEFT]:
                    print("Left")
                    ser.write(b'3')

                else:
                    ser.write(b'0')


def get_input():
    key_in = pygame.key.get_pressed()

    # Only collect when moving forward
    if key_in[pygame.K_UP]:
        if key_in[pygame.K_LEFT]:
            return 'left'
        elif key_in[pygame.K_RIGHT]:
            return 'right'
        else:
            return 'straight'

    else:
        return 'stationary'


def get_train_images():
    class GetTrainImages(object):

        def __init__(self):
            self.server_socket = socket.socket()
            self.server_socket.bind(('192.168.1.14', 8000))
            self.server_socket.listen(0)
            self.connection = self.server_socket.accept()[0].makefile('rb')

            self.send_inst = True

            self.collect_images()



        def collect_images(self):
            print('collecting images')
            label_array = np.zeros(1)
            left_array = np.zeros(1)
            right_array = 1*np.ones(1)
            straight_array = 2*np.ones(1)

            frame_num = 1

            try:
                stream_bytes = ' '

                while self.send_inst:
                    # Read the length of image, if 0 break
                    image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break

                    # Check for exit command
                    key_in = pygame.key.get_pressed()
                    if key_in[pygame.K_q]:
                        break

                    # Construct stream and read image from connection
                    image_stream = io.BytesIO()
                    image_stream.write(self.connection.read(image_len))

                    # Show video feed
                    data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
                    image = cv2.imdecode(data, 0)
                    try:
                        cv2.imshow('image', image)
                        cv2.waitKey(1)
                    except:
                        print("error displaying image")

                    # Get input from pygame
                    user_input = get_input()

                    # Add to label_array
                    if user_input is not 'stationary':
                        if user_input is 'left':
                            label_array = np.append(label_array, left_array, axis=0)
                        elif user_input is 'right':
                            label_array = np.append(label_array, right_array, axis=0)
                        elif user_input is 'straight':
                            label_array = np.append(label_array, straight_array, axis=0)

                        # Save frame
                        cv2.imwrite(folder + '/' + str(frame_num) + '.jpg', image)
                        frame_num += 1

            except IOError as e:
                print(e)

            label_array = np.delete(label_array, 0)
            np.save(folder + '/labels.npy', label_array)

    GetTrainImages()


try:

    # thread.start_new_thread(stream_video())
    # thread.start_new_thread(rc_controller())
    threading.Thread(target=get_train_images).start()
    threading.Thread(target=rc_controller).start()

except:
    print("Unable to start new thread")

while True:
    pass
