import pygame
import draw
import math
import ctypes
import sys
from classes import Node, TextInput


class Game:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self.bg_color = (100, 100, 240, 0.5)
        self.info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = self.info.current_w, self.info.current_h
        self.nodes = []
        self.active_node = None
        self.place_node_bool = None
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')
        self.text_input = TextInput()
    
    def quit_func(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def select_node(self, event):
        self.active_node = None
        for node in self.nodes:
            node.clicked(event.pos)
            if node.state:
                self.active_node = node
        
    def on_click(self, event):
        self.text_input.clicked(event)
        if not self.text_input.state:
            self.select_node(event)
            if self.active_node == None:
                self.nodes.append(Node(event))
    
    def on_keypress(self, event):
        if event.key == pygame.K_RETURN and self.active_node != None:
            self.active_node.set_weight(self.text_input.user_text)
        else:
            self.text_input.input(event)
            
    def draw(self):
        self.window.fill(self.bg_color)

        for node in self.nodes:
            node.draw(self.window)
            
        self.text_input.draw(self.window)

        pygame.display.update()

    def main(self):
        while True:
            for event in pygame.event.get():
                self.quit_func(event)
                if event.type == pygame.KEYDOWN:
                    self.on_keypress(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event)
            self.draw()
            

if __name__ == "__main__":
    game = Game()
    game.main()
