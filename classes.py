import pygame


class Button:
    def __init__(self, rect, text, identifier):
        self.rect = rect
        self.text = text
        self.identifier = identifier
        self.func = None
        self.args = None

        self.state = False

        self.color_text = pygame.Color("black")
        self.color_passive = pygame.Color("white")
        self.color_active = pygame.Color("yellow")

        self.text_surface = None
        self.text_font = pygame.font.Font(None, 32)

    def register_callback(self, func, *args):
        self.func = func
        self.args = args

    def callback(self):
        return self.func(*self.args)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self, window):
        if self.state:
            pygame.draw.rect(window, self.color_active, self.rect)
        else:
            pygame.draw.rect(window, self.color_passive, self.rect)

        self.text_surface = self.text_font.render(self.text, True, self.color_text)
        window.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(100, self.text_surface.get_width() + 10)


class TextInput:
    def __init__(self):
        self.user_text = ""
        self.rect = pygame.Rect(200, 200, 140, 32)
        self.state = False

        self.color_passive = pygame.Color("chartreuse4")
        self.color_active = pygame.Color("chartreuse3")
        self.color_text = pygame.Color("black")

        self.text_font = pygame.font.Font(None, 32)
        self.text_surface = None

    def clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.state = True
        else:
            self.state = False

    def input(self, event):
        if self.state:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else: 
                self.user_text += event.unicode

    def draw(self, window):
        if self.state:
            pygame.draw.rect(window, self.color_active, self.rect)
        else:
            pygame.draw.rect(window, self.color_passive, self.rect)

        self.text_surface = self.text_font.render(self.user_text, True, self.color_text)
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(100, self.text_surface.get_width()+10)


class Weight:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.width = 10
        self.rect = None

        diff_x = abs(start_node.pos[1] - end_node.pos[1])
        diff_y = abs(start_node.pos[0] - end_node.pos[0])
        self.length = str(int((diff_x**2 + diff_y**2)**0.5) // 100)

        self.state = False
        self.is_searched = False
        self.is_searching = False

        self.color_active = pygame.Color("yellow")
        self.color_passive = pygame.Color("black")
        self.color_search = pygame.Color("red")
        self.color_searching = pygame.Color("green")

        self.text_font = pygame.font.Font(None, 32)
        self.text_surface = None
        self.text_color = pygame.Color("black")

    def clicked(self, pos):
        click_rect = pygame.rect.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
        return click_rect.clipline(self.start_node.pos, self.end_node.pos)
    
    def set_length(self, num):
        self.length = num

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

    def draw(self, window):
        if self.state:
            self.rect = pygame.draw.line(window, self.color_active, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searching:
            self.rect = pygame.draw.line(window, self.color_searching, self.start_node.pos, self.end_node.pos, self.width)
        elif self.is_searched:
            self.rect = pygame.draw.line(window, self.color_search, self.start_node.pos, self.end_node.pos, self.width)
        else:
            self.rect = pygame.draw.line(window, self.color_passive, self.start_node.pos, self.end_node.pos, self.width)

        self.text_surface = self.text_font.render(self.length, True, self.text_color)
        window.blit(self.text_surface, (self.rect.centerx + 10, self.rect.centery + 10))


class Node:
    def __init__(self, event, name):
        self.pos = event.pos
        self.rect = None
        self.width = 5
        self.name = name
        self.origin_name = name
        self.r = 26

        self.is_start = False
        self.is_end = False
        self.state = False

        self.weights = []

        self.color_active_start = pygame.Color("lime")
        self.color_active_end = pygame.Color("orange")
        self.color_active = pygame.Color("yellow")
        self.color_boundary = pygame.Color("black")
        self.color_passive = pygame.Color("grey")
        self.color_start = pygame.Color("limegreen")
        self.color_end = pygame.Color("red")

        self.text_surface = None
        self.text_color = pygame.Color("black")
        self.text_font = pygame.font.Font(None, 32)

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

    def draw(self, window):
        if self.state and self.is_start:
            self.rect = pygame.draw.circle(window, self.color_active_start, self.pos, self.r)
        elif self.state and self.is_end:
            self.rect = pygame.draw.circle(window, self.color_active_end, self.pos, self.r)
        elif self.state:
            self.rect = pygame.draw.circle(window, self.color_active, self.pos, self.r)
        elif self.is_start:
            self.rect = pygame.draw.circle(window, self.color_start, self.pos, self.r)
        elif self.is_end:
            self.rect = pygame.draw.circle(window, self.color_end, self.pos, self.r)
        else:
            self.rect = pygame.draw.circle(window, self.color_passive, self.pos, self.r)

        pygame.draw.circle(window, self.color_boundary, self.pos, self.r, self.width)
        self.text_surface = self.text_font.render(self.name, True, self.text_color)
        window.blit(self.text_surface, (self.rect.x + self.r / 2, self.rect.y + self.r / 2))
