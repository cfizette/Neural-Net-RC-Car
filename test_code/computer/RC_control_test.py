import numpy as np
import serial
import cv2
import pygame
from pygame.locals import *



# Set up serial communications
ser = serial.Serial(3, 115200, timeout=1)
pygame.init()
disp = pygame.display.set_mode((800, 600))

# Get keyboard input and send data
while True:
    print('hi')

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

        #else:
            #ser.write(b'0')

