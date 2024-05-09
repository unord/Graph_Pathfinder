import pygame
import ctypes
from classes import TextInput, Button
from editor import Editor


class UI:
    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self.info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = self.info.current_w, self.info.current_h
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')

        self.bg_color = (100, 100, 240, 0.5)

        self.nodes = []
        self.weights = []
        self.text_input = TextInput()
        self.graph_buttons = []
        self.algo_buttons = []

        self.graph_buttons.append(Button(pygame.Rect(400, 200, 140, 32), "start", "BUTTON_GRAPH_START"))
        self.graph_buttons.append(Button(pygame.Rect(600, 200, 140, 32), "end", "BUTTON_GRAPH_END"))

        self.algo_buttons.append(Button(pygame.Rect(800, 200, 140, 32), "Dijkstra", "BUTTON_ALGO_DIJKSTRA"))
        self.algo_buttons.append(Button(pygame.Rect(1000, 200, 140, 32), "A-Star", "BUTTON_ALGO_ASTAR"))
        self.algo_buttons.append(Button(pygame.Rect(1200, 200, 140, 32), "BFS", "BUTTON_ALGO_BFS"))

    def draw(self) -> None:
        """
        Draw the scene.

        :return: None
        """

        self.window.fill(self.bg_color)

        for weight in self.weights:
            weight.draw(self.window)

        for node in self.nodes:
            node.draw(self.window)

        for button in self.graph_buttons:
            button.draw(self.window)

        for button in self.algo_buttons:
            button.draw(self.window)

        self.text_input.draw(self.window)
        pygame.display.update()


if __name__ == "__main__":
    ui = UI()
    editor = Editor(ui)
    editor.main()
