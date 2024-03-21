import pygame
import draw
import math
import ctypes

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.FULLSCREEN)

while True:
    pass
