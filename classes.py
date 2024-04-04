import pygame


class Button:
    def __init__(self, rect, text):
        self.state = False
        self.rect = rect
        self.text = text
        self.text_surface = None
        self.text_font = pygame.font.Font(None, 32)
        self.text_color = pygame.Color("black")
        self.passive_color = pygame.Color("white")
        self.active_color = pygame.Color("yellow")

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.state = True
        else: 
            self.state = False
        return self.state
    
    def draw(self, window):
        if self.state:
            pygame.draw.rect(window, self.active_color, self.rect)
            self.text_surface = self.text_font.render(self.text, True, self.text_color)
            window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
            self.rect.w = max(100, self.text_surface.get_width()+10)
        else:
            pygame.draw.rect(window, self.passive_color, self.rect)
            self.text_surface = self.text_font.render(self.text, True, self.text_color)
            window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
            self.rect.w = max(100, self.text_surface.get_width()+10)


class TextInput:
    def __init__(self):
        self.text_font = pygame.font.Font(None, 32)
        self.user_text = ""
        self.rect = pygame.Rect(200, 200, 140, 32)
        self.active = pygame.Color("lightskyblue3")
        self.passive = pygame.Color("chartreuse4")
        self.text_color = pygame.Color("black")
        self.color = self.passive
        self.state = False
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
            self.color = self.active
        else:
            self.color = self.passive
        
        pygame.draw.rect(window, self.color, self.rect)
        self.text_surface = self.text_font.render(self.user_text, True, self.text_color)
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(100, self.text_surface.get_width()+10)


class Weight:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.width = 10
        self.length = "0"
        self.state = False
        self.active_color = pygame.Color("yellow")
        self.passive_color = pygame.Color("black")
        self.rect = None
        self.text_font = pygame.font.Font(None, 32)
        self.text_surface = None
        self.text_color = pygame.Color("black")

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def set_length(self, num):
        self.length = num

    def draw(self, window):
        if self.state:
            self.rect = pygame.draw.line(window, self.active_color, self.start_node.pos, self.end_node.pos, self.width)
            self.text_surface = self.text_font.render(self.length, True, self.text_color)
            window.blit(self.text_surface, (self.rect.centerx + 10, self.rect.centery + 10))
        else:
            self.rect = pygame.draw.line(window, self.passive_color, self.start_node.pos, self.end_node.pos, self.width)
            self.text_surface = self.text_font.render(self.length, True, self.text_color)
            window.blit(self.text_surface, (self.rect.centerx + 10, self.rect.centery + 10))


class Node:
    def __init__(self, event):
        self.pos = event.pos
        self.color_active = pygame.Color("yellow")
        self.color_boundry = pygame.Color("black")
        self.color_passive = pygame.Color("grey")
        self.rect = None
        self.width = 5
        self.name = "A"
        self.r = 26
        self.state = False
        self.text_surface = None
        self.text_color = pygame.Color("black")
        self.text_font = pygame.font.Font(None, 32)
        self.weights = []

    def set_name(self, name):
        self.name = name

    def add_weight(self, weight):
        self.weights.append(weight)

    def remove_weight(self, weight):
        if weight in self.weights:
            self.weights.remove(weight)
    
    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, window):
        if self.state:
            self.rect = pygame.draw.circle(window, self.color_active, self.pos, self.r)
            pygame.draw.circle(window, self.color_boundry, self.pos, self.r, self.width)
            self.text_surface = self.text_font.render(self.name, True, self.text_color)
            window.blit(self.text_surface, (self.rect.x + self.r/2, self.rect.y + self.r/2))
        else:
            self.rect = pygame.draw.circle(window, self.color_passive, self.pos, self.r)
            pygame.draw.circle(window, self.color_boundry, self.pos, self.r, self.width)
            self.text_surface = self.text_font.render(self.name, True, self.text_color)
            window.blit(self.text_surface, (self.rect.x + self.r/2, self.rect.y + self.r/2))
