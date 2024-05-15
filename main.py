import pygame
import ctypes
from uiobjects import TextInput, Button, TextLabel, Line, Mask
from editor import Editor
from math import ceil
from typing import Callable


class UI:
    """
    UI-class that is responsible for drawing, scaling and keeping track of UI-objects.
    UI-objects are passed to scenes via UI-object, where they can attach callbacks and such.

    The UI-class also provides the ability to scale the UI to any resolution.
    It distinguishes between virtual and real coordinates and sizes.
        Virtual coordinates map to the default 1080p sizes.
        Real coordinates map to the actual resolution of the screen.
    The class provides methods for translating between these coordinates.
    These methods are baked into alternatives to pygame.draw.rect etc.
    These methods can be called using virtual coordinates, and will then be translated before rendering.
    This removes the need for every part of the program to known the size of the screen.

    Attributes:
        base_width: Default width of UI
        base_height: Default height of UI
        background_color: Background color of UI
        rect_attr: Dict describing rect-properties and their axis of dependence
    """

    base_width = 1920
    base_height = 1080

    background_color = (100, 100, 240, 0.5)

    """
    Describes axis of dependence for different rect properties
        0: Horizontal
        1: Vertical
        2: (Horizontal, Vertical)
    Used to correctly translate virtual and real coordinates.
    """
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
        """ Initializes the UI-object along with standard pygame startup-procedures. """

        # Disables windows UI-scaling to get real resolution from pygames display-info
        ctypes.windll.user32.SetProcessDPIAware()

        # Initialize pygame in fullscreen with resolution matching the screens
        pygame.init()
        self.info = pygame.display.Info()
        self.width, self.height = self.info.current_w, self.info.current_h
        self.window = pygame.display.set_mode((self.width, self.height), flags=pygame.FULLSCREEN)
        pygame.display.set_caption('Graph Visualizer')

        # Lists to keep UI-objects
        self.nodes = []
        self.weights = []
        self.text_labels = []
        self.graph_buttons = []
        self.algo_buttons = []
        self.timeline_buttons = []
        self.general_buttons = []
        self.lines = []
        self.masks = []

        self.text_input = TextInput(self, pygame.Rect(50, 370, 120, 40))

        self.text_labels.append(TextLabel(self, pygame.Rect(50, 30, 120, 40), "General:"))
        self.text_labels.append(TextLabel(self, pygame.Rect(50, 180, 120, 40), "Graph:"))
        self.text_labels.append(TextLabel(self, pygame.Rect(50, 490, 120, 40), "Algorithms:"))
        self.text_labels.append(TextLabel(self, pygame.Rect(50, 850, 120, 40), "Timeline:"))

        self.general_buttons.append(Button(self, pygame.Rect(50, 70, 120, 40), "Exit", "BUTTON_GEN_EXIT"))

        self.graph_buttons.append(Button(self, pygame.Rect(50, 220, 120, 40), "Start", "BUTTON_GRAPH_START"))
        self.graph_buttons.append(Button(self, pygame.Rect(50, 270, 120, 40), "End", "BUTTON_GRAPH_END"))
        self.graph_buttons.append(Button(self, pygame.Rect(50, 320, 120, 40), "Delete", "BUTTON_GRAPH_DELETE"))

        self.algo_buttons.append(Button(self, pygame.Rect(50, 530, 120, 40), "Dijkstra", "BUTTON_ALGO_DIJKSTRA"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 580, 120, 40), "A-Star", "BUTTON_ALGO_ASTAR"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 630, 120, 40), "BFS", "BUTTON_ALGO_BFS"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 680, 120, 40), "DFS", "BUTTON_ALGO_DFS"))
        self.algo_buttons.append(Button(self, pygame.Rect(50, 730, 120, 40), "Greedy", "BUTTON_ALGO_GREEDY"))

        self.timeline_buttons.append(Button(self, pygame.Rect(50, 890, 120, 40), "Forward", "BUTTON_TIME_FORWARD"))
        self.timeline_buttons.append(Button(self, pygame.Rect(50, 940, 120, 40), "Back", "BUTTON_TIME_BACK"))
        self.timeline_buttons.append(Button(self, pygame.Rect(50, 990, 120, 40), "Stop", "BUTTON_TIME_STOP"))

        self.lines.append(Line(self, (220, 0), (220, self.base_height)))
        self.lines.append(Line(self, (0, 150), (220, 150)))
        self.lines.append(Line(self, (0, 460), (220, 460)))
        self.lines.append(Line(self, (0, 820), (220, 820)))

        self.masks.append(Mask(self, pygame.Rect(0, 150, 220, 310), "MASK_GRAPH_BUTTONS"))
        self.masks.append(Mask(self, pygame.Rect(0, 460, 220, 360), "MASK_ALGO_BUTTONS"))
        self.masks.append(Mask(self, pygame.Rect(0, 820, 220, self.base_height - 820), "MASK_TIME_BUTTONS"))

    def get_virtual_cords(self, real_cords: tuple[int, int]) -> tuple[float, float]:
        """
        Converts real coordinates to virtual coordinates.

        :param real_cords: Real coordinates
        :return: Virtual coordinates
        """

        return real_cords[0] * self.base_width / self.width, real_cords[1] * self.base_height / self.height

    def get_real_cords(self, virtual_cords: tuple[int, int]) -> tuple[float, float]:
        """
        Converts virtual coordinates to real coordinates.

        :param virtual_cords: Virtual coordinates
        :return: Real coordinates
        """

        return virtual_cords[0] * self.width / self.base_width, virtual_cords[1] * self.height / self.base_height

    def get_real_horizontal(self, virtual_horizontal: int) -> float:
        """
        Translates virtual horizontal coordinate or length to real coordinate or length.

        :param virtual_horizontal: Virtual coordinate or length
        :return: Real coordinate or length
        """

        return virtual_horizontal * self.width / self.base_width

    def get_real_vertical(self, virtual_vertical: int) -> float:
        """
        Translates virtual vertical coordinate or length to real coordinate or length.

        :param virtual_vertical: Virtual coordinate or length
        :return: Real coordinate or length
        """

        return virtual_vertical * self.height / self.base_height

    def get_virtual_rect(self, real_rect: pygame.Rect) -> pygame.Rect:
        """
        Converts a pygame rect based on real coordinates to one based on virtual coordinates.

        :param real_rect: Real rect
        :return: Virtual rect
        """

        return pygame.Rect(
            real_rect.left * self.base_width / self.width,
            real_rect.top * self.base_height / self.height,
            real_rect.width * self.base_width / self.width,
            real_rect.height * self.base_height / self.height
        )

    def get_real_rect(self, virtual_rect: pygame.Rect) -> pygame.Rect:
        """
        Converts a pygame rect based on virtual coordinates to one based on real coordinates.

        :param virtual_rect: Virtual rect
        :return: Real rect
        """

        return pygame.Rect(
            virtual_rect.left * self.width / self.base_width,
            virtual_rect.top * self.height / self.base_height,
            virtual_rect.width * self.width / self.base_width,
            virtual_rect.height * self.height / self.base_height
        )

    def get_real_max(self, virtual_length: int) -> float:
        """
        Converts a virtual coordinate or length to a real coordinate or length,
        by scaling to the larger virtual/real ratio between horizontal and vertical.

        :param virtual_length: Virtual coordinate or length
        :return: Real coordinate or length
        """

        scale = max(self.width / self.base_width, self.height / self.base_height)
        return virtual_length * scale

    def get_real_min(self, virtual_length: int) -> float:
        """
        Converts a virtual coordinate or length to a real coordinate or length,
        by scaling to the smaller virtual/real ratio between horizontal and vertical.

        :param virtual_length: Virtual coordinate or length
        :return: Real coordinate or length
        """

        scale = min(self.width / self.base_width, self.height / self.base_height)
        return virtual_length * scale

    def get_real_avg(self, virtual_length: int) -> float:
        """
        Converts a virtual coordinate or length to a real coordinate or length,
        by scaling to the average virtual/real ratio between horizontal and vertical.

        :param virtual_length: Virtual coordinate or length
        :return: Real coordinate or length
        """

        scale = (self.width / self.base_width + self.height / self.base_height) / 2
        return virtual_length * scale

    def draw_rect(self, color: pygame.Color, rect: pygame.Rect, width: int = 0) -> pygame.Rect:
        """
        Draw a rect based on its virtual rect.

        :param color: Color of the rect
        :param rect: Virtual rect
        :param width: Virtual width of border
        :return: Virtual rect bounding changed pixels
        """

        real_rect = pygame.draw.rect(
            self.window,
            color,
            self.get_real_rect(rect),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def draw_line(self, color: pygame.Color, start_pos: tuple[int, int], end_pos: tuple[int, int], width: int = 1) -> pygame.Rect:
        """
        Draw a line based on its virtual coordinates.

        :param color: Color of the line
        :param start_pos: Virtual start position
        :param end_pos: Virtual end position
        :param width: Virtual width of line
        :return: Virtual rect bounding changed pixels
        """

        real_rect = pygame.draw.line(
            self.window,
            color,
            self.get_real_cords(start_pos),
            self.get_real_cords(end_pos),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def draw_circle(self, color: pygame.Color, center: tuple[int, int], radius: int, width: int = 0) -> pygame.Rect:
        """
        Draw a circle based on its virtual coordinates.

        :param color: Color of the circle
        :param center: Virtual center of the circle
        :param radius: Virtual radius of the circle
        :param width: Virtual width of the circle
        :return: Virtual rect bounding changed pixels
        """

        real_rect = pygame.draw.circle(
            self.window,
            color,
            self.get_real_cords(center),
            self.get_real_max(radius),
            ceil(self.get_real_max(width))
        )

        return self.get_virtual_rect(real_rect)

    def get_font(self, file_path=None, size=12) -> pygame.font.Font:
        """
        Generate a font object from virtual size.

        :param file_path: Path to font file
        :param size: Virtual size of font
        :return: Font object
        """

        return pygame.font.Font(file_path, int(self.get_real_avg(size)))

    def get_real_rect_attr(self, virtual_attr: dict[str: int]) -> dict[str: float]:
        """
        Convert pygame rect attributes from virtual to real.

        :param virtual_attr: Virtual rect attributes
        :return: Real rect attributes
        """

        real_attr = {}

        for k, v in virtual_attr.items():
            if k not in self.rect_attr:
                real_attr[k] = v
                continue

            # Use property map to correctly convert rect properties
            if self.rect_attr[k] == 0:
                real_attr[k] = self.get_real_horizontal(v)
            elif self.rect_attr[k] == 1:
                real_attr[k] = self.get_real_vertical(v)
            else:
                real_attr[k] = self.get_real_cords(v)

        return real_attr

    @staticmethod
    def font_render(font: pygame.font.Font, text: str, antialias: bool, color: pygame.Color) -> pygame.Surface:
        """
        Wrapper function to font.render.

        :param font: Font to render with
        :param text: Text to render
        :param antialias: Enable antialiasing
        :param color: Color of text
        :return: Surface with text
        """

        return font.render(text, antialias, color)

    def font_get_rect(self, text_surface: pygame.Surface, **rect_attr: dict[str: int]) -> pygame.Rect:
        """
        Get rect from text surface using virtual rect properties.

        :param text_surface: Surface to use
        :param rect_attr: Virtual rect properties
        :return: Virtual surface rect
        """

        rect_attr = self.get_real_rect_attr(rect_attr)
        real_rect = text_surface.get_rect(**rect_attr)
        return self.get_virtual_rect(real_rect)

    def blit(self, source: pygame.Surface, dest: pygame.Rect | tuple, area: pygame.Rect | tuple = None) -> None:
        """
        Blit a surface to the screen using virtual coordinates.

        :param source: Surface to draw
        :param dest: Virtual coordinates to draw surface
        :param area: Virtual rect bounding part of source to draw
        :return: None
        """

        if isinstance(dest, pygame.Rect):
            dest = self.get_real_rect(dest)
        elif isinstance(dest, tuple):
            dest = self.get_real_cords(dest)

        if isinstance(area, tuple):
            area = pygame.Rect(area)
        if isinstance(area, pygame.Rect):
            area = self.get_real_rect(area)

        self.window.blit(source, dest, area)

    def get_surface(self, size: tuple[int, int], flags: int = 0) -> pygame.Surface:
        """
        Generate surface from virtual size.

        :param size: Virtual size
        :param flags: pygame flags
        :return: Real surface
        """

        surface = pygame.Surface(self.get_real_cords(size), flags)
        return surface

    def apply_callbacks(self, **callbacks: dict[str: Callable]) -> None:
        """
        Apply callbacks to buttons from pairs of identifiers and functions.

        :param callbacks: Dict of identifiers and callbacks
        :return: None
        """

        for button in self.graph_buttons:
            if button.identifier in callbacks:
                button.register_callback(callbacks[button.identifier])

        for button in self.algo_buttons:
            if button.identifier in callbacks:
                button.register_callback(callbacks[button.identifier])

        for button in self.timeline_buttons:
            if button.identifier in callbacks:
                button.register_callback(callbacks[button.identifier])

        for button in self.general_buttons:
            if button.identifier in callbacks:
                button.register_callback(callbacks[button.identifier])

    def apply_masks(self, **masks: dict[str: bool]) -> None:
        """
        Apply mask states from pairs of identifiers and states.

        :param masks: Dict of identifiers and mask states
        :return: None
        """

        for mask in self.masks:
            if mask.identifier in masks:
                mask.state = masks[mask.identifier]

    def draw(self) -> None:
        """
        Draws the scene by calling UI-object draw functions and updating the screen.

        :return: None
        """

        self.window.fill(self.background_color)

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

        for button in self.general_buttons:
            button.draw()

        for label in self.text_labels:
            label.draw()

        for line in self.lines:
            line.draw()

        self.text_input.draw()

        for mask in self.masks:
            mask.draw()

        pygame.display.update()


if __name__ == "__main__":
    ui = UI()
    editor = Editor(ui)
    editor.main()
