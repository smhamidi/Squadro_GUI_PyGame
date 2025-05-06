import pygame
import math
from utils.components import place_player_pawns

pygame.init()

# Finding the host display information
display_info = pygame.display.Info()
MAX_WIDTH = display_info.current_w
MAX_HEIGHT = display_info.current_h


# Setting the game display
pygame.display.set_caption("Squadro by smhamidi")
GAME_WIDTH = (MAX_WIDTH * 80) // 100
GAME_HEIGHT = GAME_WIDTH // 2
DISPLAY = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
# --- Display Style
DISPLAY.fill((245, 245, 245))
print(GAME_WIDTH, GAME_HEIGHT)


# Game Board
MAIN_BOARD = pygame.image.load("./Assets/MainBoard.png")
MAIN_BOARD = pygame.transform.scale(MAIN_BOARD, (GAME_HEIGHT, GAME_HEIGHT))  # resizing
# --- Positioning the Board
MAIN_BOARD_RECT = MAIN_BOARD.get_rect()
MAIN_BOARD_RECT.topleft = (GAME_HEIGHT // 2, 0)


# Info box
# --- Constants
INFOSECTION_WIDTH = GAME_WIDTH // 4
INFOSECTION_HEIGHT = GAME_HEIGHT
INFOBOX_WIDTH = math.floor(INFOSECTION_WIDTH * 0.90)
INFOBOX_HEIGHT = math.floor(INFOSECTION_HEIGHT * 0.3)
INFOBOX_RADIUS = 20
INFOBOX_THICKNESS = 4
INFOBOX_COLOR = (0, 0, 0)

# --- Player 1 info box
PLAYER1_BOX_TOPLEFT = (
    math.floor(INFOSECTION_WIDTH * 0.05),
    math.floor(INFOSECTION_WIDTH * 0.05),
)
PLAYER1_BOX = pygame.Rect(PLAYER1_BOX_TOPLEFT, (INFOBOX_WIDTH, INFOBOX_HEIGHT))


# --- Player 2 info box
PLAYER2_BOX_TOPLEFT = (
    math.floor(INFOSECTION_WIDTH * 0.05) + math.floor(GAME_WIDTH * 0.75),
    math.floor(INFOSECTION_WIDTH * 0.05),
)
PLAYER2_BOX = pygame.Rect(PLAYER2_BOX_TOPLEFT, (INFOBOX_WIDTH, INFOBOX_HEIGHT))


# Game states
running = True
blit_objs = {"MAIN_BOARD": (MAIN_BOARD, MAIN_BOARD_RECT)}
# --- 1st Player states
PLAYER1_PAWNS = [
    {"number": 1, "position": 2, "return": True},
    {"number": 2, "position": 0, "return": False},
    {"number": 3, "position": 0, "return": False},
    {"number": 4, "position": 0, "return": False},
    {"number": 5, "position": 3, "return": False},
]
PLAYER1_COLOR = (191, 144, 0)
player1_ip = ""
player1_port = ""

# --- 2nd Player states
PLAYER2_PAWNS = [
    {"number": 1, "position": 6, "return": False},
    {"number": 2, "position": 6, "return": False},
    {"number": 3, "position": 1, "return": True},
    {"number": 4, "position": 6, "return": False},
    {"number": 5, "position": 6, "return": False},
]
PLAYER2_COLOR = (192, 0, 0)
player2_ip = ""
player2_port = ""


# Game Clock
FPS = 60
CLOCK = pygame.time.Clock()


# Main Game Loop
while running:
    # Clicking exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blitting Objects
    for key, value in blit_objs.items():
        DISPLAY.blit(value[0], value[1])

    # Players info box rects
    pygame.draw.rect(
        DISPLAY,
        PLAYER1_COLOR,
        PLAYER1_BOX,
        border_radius=INFOBOX_RADIUS,
        width=INFOBOX_THICKNESS,
    )
    pygame.draw.rect(
        DISPLAY,
        PLAYER2_COLOR,
        PLAYER2_BOX,
        border_radius=INFOBOX_RADIUS,
        width=INFOBOX_THICKNESS,
    )

    # Placing the pawns
    place_player_pawns(1, PLAYER1_PAWNS, DISPLAY, GAME_WIDTH, GAME_HEIGHT)
    place_player_pawns(2, PLAYER2_PAWNS, DISPLAY, GAME_WIDTH, GAME_HEIGHT)

    # Updating the display
    pygame.display.update()

    # Using Clock for ensuring 60fps
    CLOCK.tick(FPS)

# Quit pygame
pygame.quit()
