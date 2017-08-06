import numpy as np
import cv2
import io
import socket
import struct
from PIL import Image


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
                print('hello')
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