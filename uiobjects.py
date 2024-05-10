import pygame


class Mask:
    color_active = pygame.Color("red")
    color_passive = pygame.Color("black")

    color_active.a = 0
    color_passive.a = 90

    def __init__(self, ui, rect, identifier):
        self.ui = ui
        self.rect = rect
        self.identifier = identifier

        self.state = False

        self.surf_active = self.ui.get_surface(rect.size, pygame.SRCALPHA)
        self.surf_active.fill(self.color_active)

        self.surf_passive = self.ui.get_surface(rect.size, pygame.SRCALPHA)
        self.surf_passive.fill(self.color_passive)

    def draw(self):
        if self.state:
            self.ui.blit(self.surf_active, self.rect)
        else:
            self.ui.blit(self.surf_passive, self.rect)


class Line:
    color_body = pygame.Color("black")

    width = 3

    def __init__(self, ui, start_pos, end_pos):
        self.ui = ui
        self.start_pos = start_pos
        self.end_pos = end_pos

    def draw(self):
        self.ui.draw_line(self.color_body, self.start_pos, self.end_pos, self.width)


class TextLabel:
    color_text = pygame.Color("black")

    def __init__(self, ui, rect, text):
        self.ui = ui
        self.rect = rect
        self.text = text

        text_font = self.ui.get_font(None, 32)
        self.text_surface = self.ui.font_render(text_font, self.text, True, self.color_text)
        self.text_rect = self.ui.font_get_rect(self.text_surface, center=self.rect.center)

    def draw(self):
        self.ui.blit(self.text_surface, self.text_rect)


class Button:
    color_text = pygame.Color("black")
    color_body = pygame.Color("white")
    color_border = pygame.Color("black")

    def __init__(self, ui, rect, text, identifier):
        self.ui = ui
        self.rect = rect
        self.text = text
        self.identifier = identifier
        self.func = None
        self.args = None

        text_font = self.ui.get_font(None, 32)
        self.text_surface = self.ui.font_render(text_font, self.text, True, self.color_text)
        self.text_rect = self.ui.font_get_rect(self.text_surface, center=self.rect.center)

    def register_callback(self, func, *args):
        self.func = func
        self.args = args

    def callback(self):
        return self.func(*self.args)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self):
        self.ui.draw_rect(self.color_body, self.rect)
        self.ui.draw_rect(self.color_border, self.rect, width=2)
        self.ui.blit(self.text_surface, self.text_rect)


class TextInput:
    color_passive = pygame.Color("chartreuse4")
    color_active = pygame.Color("chartreuse3")
    color_text = pygame.Color("black")
    color_border = pygame.Color("black")

    def __init__(self, ui, rect):
        self.ui = ui
        self.user_text = ""
        self.rect = rect
        self.state = False

        self.text_font = self.ui.get_font(None, 32)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def input(self, event):
        if self.state:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else: 
                self.user_text += event.unicode

    def draw(self):
        if self.state:
            self.ui.draw_rect(self.color_active, self.rect)
        else:
            self.ui.draw_rect(self.color_passive, self.rect)

        self.ui.draw_rect(self.color_border, self.rect, width=2)

        text_surface = self.ui.font_render(self.text_font, self.user_text, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, centery=self.rect.centery, left=self.rect.left + 6)
        self.ui.blit(text_surface, text_rect, (max(text_rect.w - self.rect.w + 12, 0), 0, self.rect.w, self.rect.h))


class Weight:
    color_active = pygame.Color("yellow")
    color_passive = pygame.Color("black")
    color_search = pygame.Color("red")
    color_searching = pygame.Color("green")
    color_text = pygame.Color("black")

    width = 10
    offset = 20

    def __init__(self, ui, start_node, end_node):
        self.ui = ui
        self.start_node = start_node
        self.end_node = end_node
        self.rect = None

        diff_x = abs(start_node.pos[0] - end_node.pos[0])
        diff_y = abs(start_node.pos[1] - end_node.pos[1])
        self.length = str(int((diff_x**2 + diff_y**2)**0.5) // 100)

        self.state = False
        self.is_searched = False
        self.is_searching = False

        self.text_font = self.ui.get_font(None, 32)

    def clicked(self, pos):
        click_rect = pygame.rect.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
        return click_rect.clipline(self.start_node.pos, self.end_node.pos)
    
    def set_length(self, num):
        if num.isnumeric():
            self.length = num

    def is_similar(self, node1, node2):
        if node1 == self.start_node and node2 == self.end_node:
            return True

        if node2 == self.start_node and node1 == self.end_node:
            return True

        return False

    def set_searched(self):
        self.is_searching = False
        self.is_searched = True

    def set_searching(self):
        self.is_searched = False
        self.is_searching = True

    def get_other_node(self, node):
        if node is self.start_node:
            return self.end_node
        return self.start_node

    def set_default(self):
        self.is_searched = False
        self.is_searching = False
        self.state = False

    def draw(self):
        if self.state:
            self.rect = self.ui.draw_line(self.color_active, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searching:
            self.rect = self.ui.draw_line(self.color_searching, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searched:
            self.rect = self.ui.draw_line(self.color_search, self.start_node.pos, self.end_node.pos, self.width)
        else:
            self.rect = self.ui.draw_line(self.color_passive, self.start_node.pos, self.end_node.pos, self.width)

        diff_x = self.end_node.pos[0] - self.start_node.pos[0]
        diff_y = self.end_node.pos[1] - self.start_node.pos[1]

        diff_m = max(abs(diff_x), abs(diff_y))

        offset_x = -diff_y / diff_m * self.offset
        offset_y = diff_x / diff_m * self.offset

        text_surface = self.ui.font_render(self.text_font, self.length, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, centerx=self.rect.centerx + offset_x, centery=self.rect.centery + offset_y)
        self.ui.blit(text_surface, text_rect)


class Node:
    color_active_start = pygame.Color("lime")
    color_active_end = pygame.Color("orange")
    color_active = pygame.Color("yellow")
    color_boundary = pygame.Color("black")
    color_passive = pygame.Color("grey")
    color_start = pygame.Color("limegreen")
    color_end = pygame.Color("red")
    color_text = pygame.Color("black")

    width = 5
    r = 32

    def __init__(self, ui, pos, name):
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

    def set_name(self, name):
        self.name = name
    
    def set_name_origin(self):
        self.name = self.origin_name

    def add_weight(self, weight):
        self.weights.append(weight)

    def remove_weight(self, weight):
        if weight in self.weights:
            self.weights.remove(weight)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def get_color(self):
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

    def draw(self):
        self.rect = self.ui.draw_circle(self.get_color(), self.pos, self.r)
        self.ui.draw_circle(self.color_boundary, self.pos, self.r, self.width)
        text_surface = self.ui.font_render(self.text_font, self.name, True, self.color_text)
        text_rect = self.ui.font_get_rect(text_surface, center=self.rect.center)
        self.ui.blit(text_surface, text_rect)
