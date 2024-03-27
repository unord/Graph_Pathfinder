import pygame
import draw
import math
import ctypes
import sys
from classes import Node, TextInput, Weight


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
        self.weights = []
        self.active_weight = None
    
    def quit_func(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def select_item(self, event):
        self.active_node = None
        self.active_weight = None
        for node in self.nodes:
            node.clicked(event.pos)
            if node.state:
                self.active_node = node
        for weight in self.weights:
            weight.clicked(event.pos)
            if weight.state:
                self.active_weight = weight
        
    def on_click(self, event):
        self.text_input.clicked(event)
        if not self.text_input.state:
            self.select_item(event)
            if self.active_node == None and self.active_weight == None:
                self.nodes.append(Node(event))
    
    def on_keypress(self, event):
        if event.key == pygame.K_RETURN:
            if self.active_node != None:
                self.active_node.set_name(self.text_input.user_text)
            elif self.active_weight != None:
                self.active_weight.set_length(self.text_input.user_text)
        elif event.key == pygame.K_DELETE:
            if self.active_node != None:
                self.nodes.remove(self.active_node)
                self.active_node = None
            else:
                self.nodes = self.nodes[:-1]
        else:
            self.text_input.input(event)

    def set_weight(self, event):
        if self.active_node != None:
            for node in self.nodes:
                if node is not self.active_node:
                    if node.rect.collidepoint(event.pos):
                        self.weights.append(Weight(self.active_node, node))
            
    def draw(self):
        self.window.fill(self.bg_color)
        for weight in self.weights:
            weight.draw(self.window)
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
                if event.type == pygame.MOUSEBUTTONUP:
                    self.set_weight(event)

            self.draw()
            

if __name__ == "__main__":
    game = Game()
    game.main()
