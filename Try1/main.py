import pygame
import sys
from UI.images.buttons.button import Button
from Game.playScreen import singlePlayer
import Game.GameMain

pygame.init()

playing = False

screen_width = 1280
screen_height = 720

SCREEN = pygame.display.set_mode((screen_width, screen_height))

# Denumire fereastra
pygame.display.set_caption("Chessbinator")

BACKGROUND = pygame.image.load("UI/images/background/background.png")


def get_font(size):
    return pygame.font.Font("UI/fonts/SansSerif.ttf", size)


def main_menu():
    pygame.display.set_caption("Main Menu")

    # Game loop
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("CHESSBINATOR", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        play_button_surface = pygame.image.load("C:/Users/simio/OneDrive/Desktop/CGP/Try1/UI/images/buttons/button.png")
        option_button_surface = pygame.image.load("C:/Users/simio/OneDrive/Desktop/CGP/Try1/UI/images/buttons/button"
                                                  ".png")
        exit_button_surface = pygame.image.load("C:/Users/simio/OneDrive/Desktop/CGP/Try1/UI/images/buttons/button.png")

        play_button_surface = pygame.transform.scale(play_button_surface, (300, 100))
        option_button_surface = pygame.transform.scale(option_button_surface, (200, 100))
        exit_button_surface = pygame.transform.scale(exit_button_surface, (100, 100))

        PLAY_BUTTON = Button(image=play_button_surface, x_pos=640, y_pos=250, text_input="PLAY",
                             font=get_font(40), base_color="#2F304A",
                             hover="White")
        OPTION_BUTTON = Button(image=option_button_surface, x_pos=640, y_pos=400,
                               text_input="OPTION", font=get_font(40), base_color="#2F304A",
                               hover="White")
        EXIT_BUTTON = Button(image=exit_button_surface, x_pos=640, y_pos=550,
                             text_input="EXIT", font=get_font(40), base_color="#2F304A",
                             hover="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTION_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTION_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("options")
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("quit")
                    sys.exit()

        pygame.display.update()

def play():
    playing = True
    pygame.display.set_caption("Play")
    while playing:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        play_button_surface = pygame.image.load("UI\\images\\buttons\\button.png")
        play_button_surface = pygame.transform.scale(play_button_surface, (300, 100))

        PLAY_BACK = Button(image=None, x_pos=640, y_pos=460,
                           text_input="BACK", font=get_font(75), base_color="White", hover="White")
        PLAY_SGP = Button(image=play_button_surface, x_pos=400, y_pos=260,
                          text_input="Singleplayer", font=get_font(75), base_color="White", hover="White")
        PLAY_MP = Button(image=play_button_surface, x_pos=900, y_pos=260,
                         text_input="Multiplayer", font=get_font(75), base_color="White", hover="White")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        PLAY_SGP.changeColor(PLAY_MOUSE_POS)
        PLAY_SGP.update(SCREEN)
        PLAY_MP.changeColor(PLAY_MOUSE_POS)
        PLAY_MP.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if PLAY_SGP.checkForInput(PLAY_MOUSE_POS):
                    singlePlayer(playing)
                if PLAY_MP.checkForInput(PLAY_MOUSE_POS):
                    Game.GameMain.main()

        pygame.display.update()
    #main_menu()


if __name__ == '__main__':
    play()