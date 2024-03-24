import pygame


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

    def is_active(self, event):
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


    def update(self, window):
        if self.state:
            self.color = self.active
        else:
            self.color = self.passive
        
        pygame.draw.rect(window, self.color, self.rect)
        self.text_surface = self.text_font.render(self.user_text, True, self.text_color)
        window.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(100, self.text_surface.get_width()+10)


class Node:
    def __init__(self, event):
        self.pos = event.pos
        self.color_g = (211, 211, 211, 1)
        self.color_b = (0, 0, 0, 1)
        self.width = 5
        self.weight = None
        self.r = 20

    def set_weight(self, num):
        self.weight = num

    def draw(self, window):
        pygame.draw.circle(window, self.color_g, self.pos, self.r)
        pygame.draw.circle(window, self.color_b, self.pos, self.r + self.width, self.width)
