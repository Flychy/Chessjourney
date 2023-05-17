import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))

pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("sans-serif", 50)

class Button():
    def __init__(self, image, x_pos, y_pos, text_input, font, base_color, hover):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.base_color = base_color
        self.hover = hover
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, [47,48,74])
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        #Blit - functie in pygame pt pus imaginea pe ecran
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    """
        Urmeaza 2 functii ce realizeaza acel effect de 'hover' atunci cand
        mouse-ul este plasat pe button.(Schimba culoarea textului)
        x = position[0] - care trebuie sa fie in limitele maxim stanga respectiv maxim dreapta
            de aici si rect.left, rect.right
        y = position[1] - care trebuie sa fie in limitele sus jos samd ---||---
    """

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "black")
        else:
            self.text = main_font.render(self.text_input, True, [47, 48, 74])

