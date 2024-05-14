import pygame


class Break:
    def __init__(self, x, y, name, size, color, back_color, text, level):
        self.x = x
        self.y = y
        self.name = name
        self.size = size
        self.color = color
        self.back_color = back_color
        self.text = text
        self.text_x = 0
        self.text_y = 0
        self.text_shift(level)
        self.hide = True

    def clicked(self):
        self.hide = False
        self.color = self.back_color


    def text_shift(self, level):
        if level == "Easy":
            self.text_x = 20
            self.text_y = 15
        elif level == "Medium":
            self.text_x = 10
            self.text_y = 5
        elif level == "Hard":
            self.text_x = 7
            self.text_y = 3

    def display_tile(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if not self.hide:
            self.text.display_fonts(screen, self.name, [self.x + self.text_x, self.y + self.text_y])
