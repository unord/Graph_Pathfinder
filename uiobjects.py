import pygame
from typing import Callable


class Mask:
    """
    UI-object to mask a certain region of the UI with surfaces.

    Attributes:
        color_active: Color for the activated mask
        color_passive: Color for the deactivated mask
    """

    color_active = pygame.Color("red")
    color_passive = pygame.Color("black")

    # Set alpha values for the colors, for now only the passive mask does anything
    color_active.a = 0
    color_passive.a = 90

    def __init__(self, ui, rect: pygame.Rect, identifier: str):
        """
        Initialize an instance of the Mask class.

        :param ui: Pointer to the owner UI-object
        :param rect: Rect to draw the mask within
        :param identifier: Identifier for scene objects
        """

        self.ui = ui
        self.rect = rect
        self.identifier = identifier

        self.state = False

        # Creates a surface with alpha capabilities and filling it with the defined colors
        self.surf_active = self.ui.get_surface(rect.size, pygame.SRCALPHA)
        self.surf_active.fill(self.color_active)

        self.surf_passive = self.ui.get_surface(rect.size, pygame.SRCALPHA)
        self.surf_passive.fill(self.color_passive)

    def draw(self) -> None:
        """
        Draw the mask using the owner UI-object.

        :return: None
        """

        if self.state:
            self.ui.blit(self.surf_active, self.rect)
        else:
            self.ui.blit(self.surf_passive, self.rect)


class Line:
    """
    UI-object simply depicting a line between two points.

    Attributes:
        color_body: Color of the line
        width: Width of the line (adjusted for 1080p)
    """

    color_body = pygame.Color("black")

    width = 3

    def __init__(self, ui, start_pos: tuple[int, int], end_pos: tuple[int, int]):
        """
        Initialize an instance of the Line class.

        :param ui: Pointer to the owner UI-object
        :param start_pos: Start coordinates
        :param end_pos: End coordinates
        """

        self.ui = ui
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self) -> None:
        """
        Draw the line using the owner UI-object.

        :return: None
        """

        self.ui.draw_line(self.color_body, self.start_pos, self.end_pos, self.width)


class TextLabel:
    """
    UI-object to draw a simple text-label.

    Attributes:
        color_text: Color to draw the text
    """

    color_text = pygame.Color("black")

    def __init__(self, ui, rect: pygame.Rect, text: str):
        """
        Initialize an instance of the TextLabel class.

        :param ui: Pointer to the owner UI-object
        :param rect: Rect to draw the label within (centered)
        :param text: Text to render in the label
        """

        self.ui = ui
        self.rect = rect
        self.text = text

        # Pre-initialize the text surface and rect, since they don't change at runtime
        text_font = self.ui.get_font(None, 32)
        self.text_surface = self.ui.font_render(text_font, self.text, True, self.color_text)
        self.text_rect = self.ui.font_get_rect(self.text_surface, center=self.rect.center)

    def draw(self) -> None:
        """
        Draw the text-label using the owner UI-object.

        :return: None
        """

        self.ui.blit(self.text_surface, self.text_rect)


class Button:
    """
    UI-object to draw a simple button with support for callback function and args.

    Attributes:
        color_text: Color to draw the text.
        color_body: Color to draw the main body.
        color_border: Color to draw the border
        border_width: Width of the border (adjusted for 1080p)
    """

    color_text = pygame.Color("black")
    color_body = pygame.Color("white")
    color_border = pygame.Color("black")

    border_width = 2

    def __init__(self, ui, rect: pygame.Rect, text: str, identifier: str):
        """
        Initialize an instance of the Button class.

        :param ui: Pointer to the owner UI-object
        :param rect: Rect to draw the button within (fills and centers text)
        :param text: Text to render in the button
        :param identifier: Identifier for scene objects
        """

        self.ui = ui
        self.rect = rect
        self.text = text
        self.identifier = identifier

        self.func = None
        self.args = None
        self.kwargs = None

        # Pre-initialize the text surface and rect, since they don't change at runtime
        text_font = self.ui.get_font(None, 32)
        self.text_surface = self.ui.font_render(text_font, self.text, True, self.color_text)
        self.text_rect = self.ui.font_get_rect(self.text_surface, center=self.rect.center)

    def register_callback(self, func: Callable, *args, **kwargs) -> None:
        """
        Register a callback function along with arguments and keyword arguments.

        :param func: Function to callback to
        :param args: Arguments for function
        :param kwargs: Keyword arguments for function
        :return: None
        """

        self.func = func
        self.args = args
        self.kwargs = kwargs

    def callback(self) -> None:
        """
        Call the given callback with the given arguments.

        :return: None
        """

        return self.func(*self.args, **self.kwargs)

    def clicked(self, pos: tuple[int, int]) -> bool:
        """
        Detect whether a given coordinate overlaps the button rect.

        :param pos: Coordinate to test
        :return: Whether the coordinate overlaps the button
        """

        return self.rect.collidepoint(pos)
    
    def draw(self) -> None:
        """
        Draw the button object using the owner UI-object.

        :return: None
        """

        self.ui.draw_rect(self.color_body, self.rect)
        self.ui.draw_rect(self.color_border, self.rect, width=self.border_width)
        self.ui.blit(self.text_surface, self.text_rect)


class TextInput:
    """
    UI-object to draw a text-input field for entering text.

    Attributes:
        color_passive: Color to use when text-input is not selected
        color_active: Color to use when text-input is selected
        color_text: Color to draw the text
        color_border: Color to draw the border
        border_width: Width of the border (adjusted for 1080p)
    """

    color_passive = pygame.Color("chartreuse4")
    color_active = pygame.Color("chartreuse3")
    color_text = pygame.Color("black")
    color_border = pygame.Color("black")

    border_width = 2

    def __init__(self, ui, rect: pygame.Rect):
        """
        Initialize an instance of the TextInput class.

        :param ui: Pointer to the owner UI-object
        :param rect: Rect to draw the text-input within (text aligned to edges)
        """

        self.ui = ui
        self.user_text = ""
        self.rect = rect
        self.state = False

        self.text_font = self.ui.get_font(None, 32)

    def clicked(self, pos: tuple[int, int]) -> bool:
        """
        Detect whether a given coordinate overlaps the input rect.

        :param pos: Coordinate to test
        :return: Whether the coordinate overlaps the input
        """

        return self.rect.collidepoint(pos)

    def input(self, event: pygame.event.Event) -> None:
        """
        Fallthrough for input picking up character inputs when state is set.

        :param event: Pygame keyboard event
        :return: None
        """

        if self.state:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else: 
                self.user_text += event.unicode

    def draw(self) -> None:
        """
        Draw the text-input using the owner UI-object.

        :return: None
        """

        if self.state:
            self.ui.draw_rect(self.color_active, self.rect)
        else:
            self.ui.draw_rect(self.color_passive, self.rect)

        self.ui.draw_rect(self.color_border, self.rect, width=self.border_width)

        # Aligns the text-surface to the left of the input
        # If it's bigger than the field itself, it will align to the right and crop the surface to fit
        text_surface = self.ui.font_render(self.text_font, self.user_text, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, centery=self.rect.centery, left=self.rect.left + 6)
        self.ui.blit(text_surface, text_rect, (max(text_rect.w - self.rect.w + 12, 0), 0, self.rect.w, self.rect.h))


class Node:
    """
    UI-class for drawing a node (or a vertex) for use in graphing.

    Attributes:
        color_active_start: Color to draw a start-node when selected
        color_active_end: Color to draw an end-node when selected
        color_active: Color to draw a node when selected
        color_boundary: Color to draw the node boundary
        color_passive: Color to draw a node when not selected
        color_start: Color to draw a start-node
        color_end: Color to draw an end-node
        color_text: Color to draw text
        border_width: Width of node border (adjusted for 1080p)
        radius: Radius of node (adjusted for 1080p)
    """

    color_active_start = pygame.Color("lime")
    color_active_end = pygame.Color("orange")
    color_active = pygame.Color("yellow")
    color_boundary = pygame.Color("black")
    color_passive = pygame.Color("grey")
    color_start = pygame.Color("limegreen")
    color_end = pygame.Color("red")
    color_text = pygame.Color("black")

    border_width = 5
    radius = 32

    def __init__(self, ui, pos: tuple[int, int], name: str):
        """
        Initialize an instance of the Node class.

        :param ui: Pointer to the owner UI-object
        :param pos: Coordinates to the node center
        :param name: Name of the node
        """

        self.ui = ui
        self.pos = pos
        self.rect = None
        self.name = name
        self.origin_name = name

        self.is_start = False
        self.is_end = False
        self.state = False

        self.weights = []

        self.text_font = self.ui.get_font(None, 32)

    def set_name(self, name: str) -> None:
        """
        Set the name of a node.

        :param name: New name
        :return: None
        """

        self.name = name

    def set_name_origin(self) -> None:
        """
        Reset the node to its original name (solver)

        :return: None
        """

        self.name = self.origin_name

    def add_weight(self, weight) -> None:
        """
        Add a weight to the nodes index of weights.

        :param weight: Weight to add
        :return: None
        """

        self.weights.append(weight)

    def remove_weight(self, weight) -> None:
        """
        Remove a weight from the nodes index of weights.

        :param weight: Weight to remove
        :return: None
        """

        if weight in self.weights:
            self.weights.remove(weight)

    def clicked(self, pos):
        """
        Detect whether a given coordinate overlaps the node (approx).
        Simplifies to a rect collision.

        :param pos: Coordinate to test
        :return: Whether the coordinate overlaps the node
        """

        return self.rect.collidepoint(pos)

    def get_color(self) -> pygame.Color:
        """
        Get the appropriate color, given the nodes current state.

        :return: Appropriate color
        """

        if self.state and self.is_start:
            return self.color_active_start
        elif self.state and self.is_end:
            return self.color_active_end
        elif self.state:
            return self.color_active
        elif self.is_start:
            return self.color_start
        elif self.is_end:
            return self.color_end
        else:
            return self.color_passive

    def draw(self) -> None:
        """
        Draw the node using the owner UI-object.

        :return: None
        """

        self.rect = self.ui.draw_circle(self.get_color(), self.pos, self.radius)
        self.ui.draw_circle(self.color_boundary, self.pos, self.radius, self.border_width)
        text_surface = self.ui.font_render(self.text_font, self.name, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, center=self.rect.center)
        self.ui.blit(text_surface, text_rect)


class Weight:
    """
    UI-object to draw a weight (or an edge) for use in graphing.

    Attributes:
        color_active: Color to draw when weight is selected
        color_passive: Color to draw when weight is not selected
        color_search: Color to draw when weight has been searched (solver)
        color_searching: Color to draw when weight is being searched (solver)
        color_text: Color to draw text
        width: Width of drawn line (adjusted for 1080p)
        offset: Text-offset from line (adjusted for 1080p)
        clip_size: Size to use for click-detection (read clicked docs)
    """

    color_active = pygame.Color("yellow")
    color_passive = pygame.Color("black")
    color_search = pygame.Color("red")
    color_searching = pygame.Color("green")
    color_text = pygame.Color("black")

    width = 10
    offset = 20

    clip_size = 30

    def __init__(self, ui, start_node: Node, end_node: Node):
        """
        Initialize an instance of the Weight class.

        :param ui: Pointer to the owner UI-object
        :param start_node: Source node
        :param end_node: Destination node
        """

        self.ui = ui
        self.start_node = start_node
        self.end_node = end_node
        self.rect = None

        # Calculate a default length for the weight, based on distance
        diff_x = abs(start_node.pos[0] - end_node.pos[0])
        diff_y = abs(start_node.pos[1] - end_node.pos[1])
        self.length = str(int((diff_x**2 + diff_y**2)**0.5) // 100)

        self.state = False
        self.is_searched = False
        self.is_searching = False

        self.text_font = self.ui.get_font(None, 32)

    def clicked(self, pos: tuple[int, int]):
        """
        Detect whether a given coordinate overlaps the weight (approx).

        :param pos: Coordinate to test
        :return: Whether the coordinate overlaps the weight
        """

        # This is a better approach to detecting clicks on rects
        # Draw a rect around the clicked area, check if the line (weight) clips it.
        click_rect = pygame.rect.Rect(pos[0] - self.clip_size / 2, pos[1] - self.clip_size / 2, self.clip_size, self.clip_size)
        return click_rect.clipline(self.start_node.pos, self.end_node.pos)
    
    def set_length(self, num: str) -> None:
        """
        Set the length of the weight.

        :param num: Length to set the weight to
        :return: None
        """

        # Filter non-numeric inputs to prevent errors
        if num.isnumeric():
            self.length = num

    def is_similar(self, node1: Node, node2: Node) -> bool:
        """
        Check whether given nodes are equivalent to own nodes.

        :param node1: Node 1
        :param node2: Node 2
        :return: Whether self and given nodes are the same (ignore order)
        """

        if node1 == self.start_node and node2 == self.end_node:
            return True

        if node2 == self.start_node and node1 == self.end_node:
            return True

        return False

    def set_searched(self) -> None:
        """
        Set weight to searched status (solver)

        :return: None
        """

        self.is_searching = False
        self.is_searched = True

    def set_searching(self) -> None:
        """
        Set weight to searching status (solver)

        :return: None
        """

        self.is_searched = False
        self.is_searching = True

    def get_other_node(self, node: Node) -> Node:
        """
        Get opposing node from given node.
        Useful when caller doesn't know, whether given node is source or dest.

        :param node: Node to use
        :return: Opposite node to given node
        """

        if node is self.start_node:
            return self.end_node
        return self.start_node

    def set_default(self) -> None:
        """
        Reset all states (solver)

        :return: None
        """

        self.is_searched = False
        self.is_searching = False
        self.state = False

    def draw(self) -> None:
        """
        Draw the weight using the owner UI-object.

        :return: None
        """

        # Draw using correct color, checking all states
        if self.state:
            self.rect = self.ui.draw_line(self.color_active, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searching:
            self.rect = self.ui.draw_line(self.color_searching, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searched:
            self.rect = self.ui.draw_line(self.color_search, self.start_node.pos, self.end_node.pos, self.width)
        else:
            self.rect = self.ui.draw_line(self.color_passive, self.start_node.pos, self.end_node.pos, self.width)

        """
        Calculate coordinates to use when drawing weight length. Simplifies to this piece of math:
            v = dest - source
            pos = c + cross(v) * (offset / |v|)
        c is the center of the line.
        """

        diff_x = self.end_node.pos[0] - self.start_node.pos[0]
        diff_y = self.end_node.pos[1] - self.start_node.pos[1]

        diff_m = max(abs(diff_x), abs(diff_y))

        offset_x = -diff_y / diff_m * self.offset
        offset_y = diff_x / diff_m * self.offset

        text_surface = self.ui.font_render(self.text_font, self.length, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, centerx=self.rect.centerx + offset_x, centery=self.rect.centery + offset_y)
        self.ui.blit(text_surface, text_rect)
