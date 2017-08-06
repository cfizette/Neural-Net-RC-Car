import pygame
import time
import win32api

key = ord('a')

pygame.init()
while True:
    time.sleep(1)
    key_in = pygame.key.get_pressedaaaa()
    if (win32api.GetKeyState(key) & (1 << 7)) != 0:
        print('a')
