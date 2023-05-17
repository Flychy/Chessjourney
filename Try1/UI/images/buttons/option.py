import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 800))

pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("sans-serif", 50)

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, [47,48,74])
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        #Blit - functie in pygame pt pus imaginea pe ecran
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    """
        Urmeaza 2 functii ce realizeaza acel effect de 'hover' atunci cand
        mouse-ul este plasat pe button.(Schimba culoarea textului)
        x = position[0] - care trebuie sa fie in limitele maxim stanga respectiv maxim dreapta
            de aici si rect.left, rect.right
        y = position[1] - care trebuie sa fie in limitele sus jos samd ---||---
    """

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            print("Button pressed!")
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "white")
        else:
            self.text = main_font.render(self.text_input, True, [47,48,74] )


#Creearea butonului
button_surface = pygame.image.load("C:/Users/simio/OneDrive/Desktop/CGP/Try1/UI/images/button.png")
button_surface = pygame.transform.scale(button_surface, (300, 100))

#Parametrii Constructorului default, ii muta pozitia pe ecran
button = Button(button_surface, 200, 300, "OPTIONS")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button.checkForInput(pygame.mouse.get_pos())

    screen.fill("white")
    button.update()
    button.changeColor(pygame.mouse.get_pos())

    pygame.display.update()