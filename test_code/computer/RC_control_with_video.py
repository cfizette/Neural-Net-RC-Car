import threading
import io
import socket
import struct
import serial
import pygame
import _thread as thread
import cv2
import numpy as np



def rc_controller():
    ser = serial.Serial(3, 115200, timeout=1)
    pygame.init()
    disp = pygame.display.set_mode((800, 600))

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


def stream_video():
    class StreamVideo(object):

        def __init__(self):
            self.server_socket = socket.socket()
            self.server_socket.bind(('192.168.1.14', 8000))
            self.server_socket.listen(0)

            self.connection = self.server_socket.accept()[0].makefile('rb')

            self.send_inst = True

            self.collect_images()

        def collect_images(self):
            print('collecting images')

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

                    # Rewind stream and open as image
                    # image_stream.seek(0)

                    data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
                    image = cv2.imdecode(data, 1)
                    try:
                        cv2.imshow('image', image)
                        cv2.waitKey(1)
                    except:
                        print("error")

                        # image = Image.open(image_stream)
                        # Image._show(image)

            except IOError as e:
                print(e)

    StreamVideo()


try:

    # thread.start_new_thread(stream_video())
    # thread.start_new_thread(rc_controller())
    threading.Thread(target=stream_video).start()
    threading.Thread(target=rc_controller).start()

except:
    print("Unable to start new thread")

while True:
    pass
