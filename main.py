import pygame
import draw
import math
import ctypes
import sys
from classes import Node, TextInput

ctypes.windll.user32.SetProcessDPIAware()
pygame.init()


def main():
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    bg_color = (100, 100, 240, 0.5)

    nodes = []

    window = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.FULLSCREEN)
    pygame.display.set_caption('Graph Visualizer')
    text_input = TextInput()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                text_input.input(event)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                text_input.is_active(event)
        
        window.fill(bg_color)

        for node in nodes:
            node.draw(window)
        
        text_input.update(window)

        pygame.display.update()

if __name__ == "__main__":
    main()
