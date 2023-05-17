import pygame
import pygame as p
import Game.GameEngine, Game.ChessAl
from UI.images.buttons.button import Button
import sys
from multiprocessing import Process, Queue

pygame.init()

screen_width = 1280
screen_height = 720

PLAY_SCREEN = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("SG Mode")

BACKGROUND = pygame.image.load("UI\\images\\background\\background.png")

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def get_font(size):
    # return pygame.font.Font("UI/fonts/SansSerif.ttf", size)
    return pygame.font.SysFont("sans-serif", 50)


def get_bold_font(size):
    # return pygame.font.Font("UI/fonts/SansSerif.ttf", size)
    return pygame.font.SysFont("sans-serif", 50, True)


def singlePlayer(game_state):
    pygame.display.set_caption("SP Mode")
    running = True
    # Game loop
    while True:
        PLAY_SCREEN.blit(BACKGROUND, (0, 0))

        PLAY_SCREEN_MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_MENU_TEXT = get_bold_font(40).render("MATCH SETTINGS", True, "white")
        PLAY_MENU_RECT = PLAY_MENU_TEXT.get_rect(center=(640, 50))

        """
         --------------------------------------------------------------------------------  
            
                                        DIFFICULTY BUTTONS
            
         --------------------------------------------------------------------------------   
        """
        difficulty_button = pygame.image.load("UI\\images\\buttons\\difficulty"
                                              ".png")
        PLAY_DIFFICULTY_TEXT = get_font(30).render("Difficulty : ", True, "white")
        PLAY_DIFFICULTY_RECT = PLAY_MENU_TEXT.get_rect(center=(340, 170))
        difficulty_level = 0

        d1 = pygame.transform.scale(difficulty_button, (50, 50))
        d2 = pygame.transform.scale(difficulty_button, (50, 50))
        d3 = pygame.transform.scale(difficulty_button, (50, 50))
        clicked_image = pygame.image.load("UI\\images\\buttons\\difficulty_clicked.png")
        D1 = Button(image=d1, x_pos=490, y_pos=170, text_input="1",
                    font=get_font(40), base_color="#2F304A",
                    hover="black")
        D2 = Button(image=d2, x_pos=640, y_pos=170,
                    text_input="2", font=get_font(40), base_color="#2F304A",
                    hover="black")
        D3 = Button(image=d3, x_pos=790, y_pos=170,
                    text_input="3", font=get_font(40), base_color="#2F304A",
                    hover="black")

        """
         --------------------------------------------------------------------------------  

                                       PLAY AS (COLOR) BUTTONS 

         --------------------------------------------------------------------------------   
        """
        play_as_button_white = pygame.image.load("UI\\images\\buttons\\play_as_white"
                                                 ".png")
        play_as_button_black = pygame.image.load("UI\\images\\buttons\\play_as_black"
                                                 ".png")

        PLAY_SIDE_TEXT = get_font(30).render("Play as : ", True, "white")
        PLAY_SIDE_RECT = PLAY_SIDE_TEXT.get_rect(center=(270, 240))
        play_color = True

        # Play as button white
        pabw = pygame.transform.scale(play_as_button_white, (50, 50))
        # Play as button black
        pabb = pygame.transform.scale(play_as_button_black, (50, 50))

        PABW = Button(image=pabw, x_pos=575, y_pos=240, text_input="",
                      font=get_font(40), base_color="#2F304A",
                      hover="black")
        PABB = Button(image=pabb, x_pos=715, y_pos=240,
                      text_input="", font=get_font(40), base_color="#2F304A",
                      hover="black")

        """
         --------------------------------------------------------------------------------  

                                       TIMMER  BUTTONS 

         --------------------------------------------------------------------------------   
        """

        # Same old white button
        timmer_button = pygame.image.load("UI\\images\\buttons\\difficulty"
                                          ".png")
        PLAY_TIMER_TEXT = get_font(30).render("Timer(min) : ", True, "white")
        PLAY_TIMER_RECT = PLAY_MENU_TEXT.get_rect(center=(340, 310))
        timer = False
        set_timer_to = 0

        t1 = pygame.transform.scale(timmer_button, (50, 50))
        t2 = pygame.transform.scale(timmer_button, (50, 50))
        t3 = pygame.transform.scale(timmer_button, (50, 50))
        clicked_image = pygame.image.load("UI\\images\\buttons\\difficulty_clicked.png")
        T1 = Button(image=t1, x_pos=490, y_pos=310, text_input="5",
                    font=get_font(40), base_color="#2F304A",
                    hover="black")
        T2 = Button(image=t2, x_pos=640, y_pos=310,
                    text_input="10", font=get_font(40), base_color="#2F304A",
                    hover="black")
        T3 = Button(image=t3, x_pos=790, y_pos=310,
                    text_input="15", font=get_font(40), base_color="#2F304A",
                    hover="black")

        """
         --------------------------------------------------------------------------------  

                                       PLAY AND BACK  BUTTONS 

         --------------------------------------------------------------------------------   
        """

        play_button = pygame.image.load("UI\\images\\buttons\\button.png")
        play_button_surface = pygame.transform.scale(play_button, (200, 100))

        PLAY = Button(image=play_button_surface, x_pos=400, y_pos=510,
                      text_input="PLAY", font=get_font(75), base_color="White", hover="White")
        BACK = Button(image=play_button_surface, x_pos=900, y_pos=510,
                      text_input="BACK", font=get_font(75), base_color="White", hover="White")

        """
            DISPLAY THE BUTTONS
        """
        PLAY.changeColor(PLAY_SCREEN_MENU_MOUSE_POS)
        PLAY.update(PLAY_SCREEN)
        BACK.changeColor(PLAY_SCREEN_MENU_MOUSE_POS)
        BACK.update(PLAY_SCREEN)
        PLAY_SCREEN.blit(PLAY_MENU_TEXT, PLAY_MENU_RECT)
        PLAY_SCREEN.blit(PLAY_DIFFICULTY_TEXT, PLAY_DIFFICULTY_RECT)
        PLAY_SCREEN.blit(PLAY_SIDE_TEXT, PLAY_SIDE_RECT)
        PLAY_SCREEN.blit(PLAY_TIMER_TEXT, PLAY_TIMER_RECT)

        for button in [D1, D2, D3]:
            button.changeColor(PLAY_SCREEN_MENU_MOUSE_POS)
            button.update(PLAY_SCREEN)
        for button in [PABW, PABB]:
            button.changeColor(PLAY_SCREEN_MENU_MOUSE_POS)
            button.update(PLAY_SCREEN)
        for button in [T1, T2, T3]:
            button.changeColor(PLAY_SCREEN_MENU_MOUSE_POS)
            button.update(PLAY_SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if D1.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    difficulty_level = 1
                    D1.image = clicked_image
                    button.update(PLAY_SCREEN)
                    print("1")
                if D2.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    difficulty_level = 2
                    D2.image = clicked_image
                    button.update(PLAY_SCREEN)
                    print("2")
                if D3.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    difficulty_level = 3
                    D3.image = clicked_image
                    button.update(PLAY_SCREEN)
                    print("3")
                if PABW.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    print("Playing as white")
                if PABB.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    color = False
                    print("Playing as black")
                if T1.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    timer = True
                    print("Selected 5 mins")
                if T2.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    timer = True
                    print("Selected 10 mins")
                if T3.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    timer = True
                    print("Selected 15 mins")
                if PLAY.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    print("sloboz")
                if BACK.checkForInput(PLAY_SCREEN_MENU_MOUSE_POS):
                    return
        pygame.display.update()
