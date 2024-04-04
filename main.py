import pygame
import draw
import math
import ctypes
import sys
from classes import Node, TextInput, Weight

ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):
        pygame.init()
        self.bg_color = (100, 100, 240, 0.5)
        self.info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = self.info.current_w, self.info.current_h
        self.nodes = []
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')
        self.text_input = TextInput()
        self.weights = []
        self.active = None
    
    def quit_func(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def set_active(self, new) -> None:
        """
        Sets the active item and handles necessary changes involved in the process.

        :param new: Item to set active
        :return:
        """

        if self.active:
            self.active.state = False

        self.active = new

        if self.active is not None:
            self.active.state = True

        if self.active is None:
            self.text_input.user_text = ""
        elif isinstance(self.active, Node):
            self.text_input.user_text = self.active.name
        else:
            self.text_input.user_text = self.active.length

    def select_item(self, event):
        for node in self.nodes:
            if node.clicked(event.pos):
                self.set_active(node)
                return False

        for weight in self.weights:
            if weight.clicked(event.pos):
                self.set_active(weight)
                return False

        res = self.active is None
        self.set_active(None)
        return res

    def on_click(self, event):
        self.text_input.clicked(event)
        if not self.text_input.state:
            if self.select_item(event):
                new = Node(event)
                self.nodes.append(new)
                # self.set_active(new)
    
    def on_keypress(self, event):
        if event.key == pygame.K_RETURN:
            if isinstance(self.active, Node):
                self.active.set_name(self.text_input.user_text)
            elif isinstance(self.active, Weight):
                self.active.set_length(self.text_input.user_text)
        elif event.key == pygame.K_DELETE:
            if isinstance(self.active, Weight):
                self.weights.remove(self.active)

                for node in self.nodes:
                    node.remove_weight(self.active)

                self.set_active(None)
                return

            elif isinstance(self.active, Node):
                deleted = self.active
                self.nodes.remove(self.active)
                self.set_active(None)

            else:
                deleted = self.nodes.pop()

            for weight in deleted.weights:
                for node in self.nodes:
                    node.remove_weight(weight)

                self.weights.remove(weight)
        else:
            self.text_input.input(event)

    def set_weight(self, event):
        if isinstance(self.active, Node):
            for node in self.nodes:
                if node is not self.active:
                    if node.rect.collidepoint(event.pos):
                        curr = Weight(self.active, node)

                        self.active.add_weight(curr)
                        node.add_weight(curr)

                        self.set_active(curr)
                        self.weights.append(curr)
            
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
