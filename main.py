import pygame
import ctypes
from uiobjects import TextInput, Button, TextLabel, Line
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
        self.text_labels = []
        self.graph_buttons = []
        self.algo_buttons = []
        self.timeline_buttons = []
        self.lines = []

        self.text_input = TextInput(pygame.Rect(50, 230, 120, 40))

        self.text_labels.append(TextLabel(pygame.Rect(50, 40, 120, 40), "Graph:"))
        self.text_labels.append(TextLabel(pygame.Rect(50, 400, 120, 40), "Algorithms:"))
        self.text_labels.append(TextLabel(pygame.Rect(50, 800, 120, 40), "Timeline:"))

        self.graph_buttons.append(Button(pygame.Rect(50, 80, 120, 40), "Start", "BUTTON_GRAPH_START"))
        self.graph_buttons.append(Button(pygame.Rect(50, 130, 120, 40), "End", "BUTTON_GRAPH_END"))
        self.graph_buttons.append(Button(pygame.Rect(50, 180, 120, 40), "Delete", "BUTTON_GRAPH_DELETE"))

        self.algo_buttons.append(Button(pygame.Rect(50, 440, 120, 40), "Dijkstra", "BUTTON_ALGO_DIJKSTRA"))
        self.algo_buttons.append(Button(pygame.Rect(50, 490, 120, 40), "A-Star", "BUTTON_ALGO_ASTAR"))
        self.algo_buttons.append(Button(pygame.Rect(50, 540, 120, 40), "BFS", "BUTTON_ALGO_BFS"))
        self.algo_buttons.append(Button(pygame.Rect(50, 590, 120, 40), "DFS", "BUTTON_ALGO_DFS"))
        self.algo_buttons.append(Button(pygame.Rect(50, 640, 120, 40), "Greedy", "BUTTON_ALGO_GREEDY"))

        self.timeline_buttons.append(Button(pygame.Rect(50, 840, 120, 40), "Forward", "BUTTON_TIME_FORWARD"))
        self.timeline_buttons.append(Button(pygame.Rect(50, 890, 120, 40), "Back", "BUTTON_TIME_BACK"))
        self.timeline_buttons.append(Button(pygame.Rect(50, 940, 120, 40), "Stop", "BUTTON_TIME_STOP"))

        self.lines.append(Line((220, 0), (220, self.HEIGHT)))

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

        for button in self.timeline_buttons:
            button.draw(self.window)

        for label in self.text_labels:
            label.draw(self.window)

        for line in self.lines:
            line.draw(self.window)

        self.text_input.draw(self.window)
        pygame.display.update()


if __name__ == "__main__":
    ui = UI()
    editor = Editor(ui)
    editor.main()
