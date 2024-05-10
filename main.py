import pygame
import ctypes
from uiobjects import TextInput, Button, TextLabel, Line
from editor import Editor
from math import ceil


class UI:
    base_width = 1920
    base_height = 1080

    bg_color = (100, 100, 240, 0.5)

    rect_attr = {
        "x": 0,
        "y": 1,
        "top": 1,
        "left": 0,
        "bottom": 1,
        "right": 0,
        "topleft": 2,
        "bottomleft": 2,
        "topright": 2,
        "bottomright": 2,
        "midtop": 2,
        "midleft": 2,
        "midbottom": 2,
        "midright": 2,
        "center": 2,
        "centerx": 0,
        "centery": 1,
        "size": 2,
        "width": 0,
        "height": 1,
        "w": 0,
        "h": 1
    }

    def __init__(self):
        ctypes.windll.user32.SetProcessDPIAware()
        pygame.init()
        self.info = pygame.display.Info()
        self.width, self.height = self.info.current_w, self.info.current_h
        self.window = pygame.display.set_mode((self.width, self.height), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')

        self.nodes = []
        self.weights = []
        self.text_labels = []
        self.graph_buttons = []
        self.algo_buttons = []
        self.timeline_buttons = []
        self.lines = []

        self.text_input = TextInput(self, pygame.Rect(50, 230, 120, 40))

        self.text_labels.append(TextLabel(self, pygame.Rect(50, 40, 120, 40), "Graph:"))
        self.text_labels.append(TextLabel(self, pygame.Rect(50, 400, 120, 40), "Algorithms:"))
        self.text_labels.append(TextLabel(self, pygame.Rect(50, 800, 120, 40), "Timeline:"))

        self.graph_buttons.append(Button(self, pygame.Rect(50, 80, 120, 40), "Start", "BUTTON_GRAPH_START"))
        self.graph_buttons.append(Button(self, pygame.Rect(50, 130, 120, 40), "End", "BUTTON_GRAPH_END"))
        self.graph_buttons.append(Button(self, pygame.Rect(50, 180, 120, 40), "Delete", "BUTTON_GRAPH_DELETE"))

        self.algo_buttons.append(Button(self, pygame.Rect(50, 440, 120, 40), "Dijkstra", "BUTTON_ALGO_DIJKSTRA"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 490, 120, 40), "A-Star", "BUTTON_ALGO_ASTAR"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 540, 120, 40), "BFS", "BUTTON_ALGO_BFS"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 590, 120, 40), "DFS", "BUTTON_ALGO_DFS"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 640, 120, 40), "Greedy", "BUTTON_ALGO_GREEDY"))

        self.timeline_buttons.append(Button(self, pygame.Rect(50, 840, 120, 40), "Forward", "BUTTON_TIME_FORWARD"))
        self.timeline_buttons.append(Button(self, pygame.Rect(50, 890, 120, 40), "Back", "BUTTON_TIME_BACK"))
        self.timeline_buttons.append(Button(self, pygame.Rect(50, 940, 120, 40), "Stop", "BUTTON_TIME_STOP"))

        self.lines.append(Line(self, (220, 0), (220, self.base_height)))

    def get_virtual_cords(self, real_cords):
        return real_cords[0] * self.base_width / self.width, real_cords[1] * self.base_height / self.height

    def get_real_cords(self, virtual_cords):
        return virtual_cords[0] * self.width / self.base_width, virtual_cords[1] * self.height / self.base_height

    def get_real_horizontal(self, virtual_horizontal):
        return virtual_horizontal * self.width / self.base_width

    def get_real_vertical(self, virtual_vertical):
        return virtual_vertical * self.height / self.base_height

    def get_virtual_rect(self, real_rect):
        return pygame.Rect(
            real_rect.left * self.base_width / self.width,
            real_rect.top * self.base_height / self.height,
            real_rect.width * self.base_width / self.width,
            real_rect.height * self.base_height / self.height
        )

    def get_real_rect(self, virtual_rect):
        return pygame.Rect(
            virtual_rect.left * self.width / self.base_width,
            virtual_rect.top * self.height / self.base_height,
            virtual_rect.width * self.width / self.base_width,
            virtual_rect.height * self.height / self.base_height
        )

    def get_real_max(self, virtual_length):
        scale = max(self.width / self.base_width, self.height / self.base_height)
        return virtual_length * scale

    def get_real_min(self, virtual_length):
        scale = min(self.width / self.base_width, self.height / self.base_height)
        return virtual_length * scale

    def get_real_avg(self, virtual_length):
        scale = (self.width / self.base_width + self.height / self.base_height) / 2
        return virtual_length * scale

    def draw_rect(self, color, rect, width=0):
        real_rect = pygame.draw.rect(
            self.window,
            color,
            self.get_real_rect(rect),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def draw_line(self, color, start_pos, end_pos, width=1):
        real_rect = pygame.draw.line(
            self.window,
            color,
            self.get_real_cords(start_pos),
            self.get_real_cords(end_pos),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def draw_circle(self, color, center, radius, width=0):
        real_rect = pygame.draw.circle(
            self.window,
            color,
            self.get_real_cords(center),
            self.get_real_max(radius),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def get_font(self, file_path=None, size=12):
        return pygame.font.Font(file_path, int(self.get_real_avg(size)))

    def get_real_rect_attr(self, virtual_attr):
        real_attr = {}

        for k, v in virtual_attr.items():
            if k not in self.rect_attr:
                real_attr[k] = v
                continue

            if self.rect_attr[k] == 0:
                real_attr[k] = self.get_real_horizontal(v)
            elif self.rect_attr[k] == 1:
                real_attr[k] = self.get_real_vertical(v)
            else:
                real_attr[k] = self.get_real_cords(v)

        return real_attr

    @staticmethod
    def font_render(font, text, antialias, color):
        return font.render(text, antialias, color)

    def font_get_rect(self, text_surface, **rect_attr):
        rect_attr = self.get_real_rect_attr(rect_attr)
        real_rect = text_surface.get_rect(**rect_attr)
        return self.get_virtual_rect(real_rect)

    def blit(self, source, dest, area=None):
        if isinstance(dest, pygame.Rect):
            dest = self.get_real_rect(dest)
        elif isinstance(dest, tuple) or isinstance(dest, list):
            dest = self.get_real_cords(dest)

        if isinstance(area, tuple) or isinstance(area, list):
            area = pygame.Rect(area)
        if isinstance(area, pygame.Rect):
            area = self.get_real_rect(area)

        self.window.blit(source, dest, area)

    def draw(self) -> None:
        """
        Draw the scene.

        :return: None
        """

        self.window.fill(self.bg_color)

        for weight in self.weights:
            weight.draw()

        for node in self.nodes:
            node.draw()

        for button in self.graph_buttons:
            button.draw()

        for button in self.algo_buttons:
            button.draw()

        for button in self.timeline_buttons:
            button.draw()

        for label in self.text_labels:
            label.draw()

        for line in self.lines:
            line.draw()

        self.text_input.draw()
        pygame.display.update()


if __name__ == "__main__":
    ui = UI()
    editor = Editor(ui)
    editor.main()
