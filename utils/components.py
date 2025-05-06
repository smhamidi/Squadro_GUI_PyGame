import pygame
import math
import os


def place_player_pawns(player_number, pawns_position, surface, game_width, game_height):
    if player_number == 1:
        DIR_PATH = os.path.dirname(__file__)
        IMAGE_PATH = os.path.join(DIR_PATH, "..", "Assets", "Player1.png")
        PAWN_WIDTH = math.floor(game_width / 16)
        PAWN_HEIGHT = math.floor(game_width / 128)
        START_POSITION = (
            math.floor(game_width / 4 + PAWN_HEIGHT),
            math.floor(1.5 * PAWN_HEIGHT + 1.5 * PAWN_WIDTH),
        )
        OFFSET = math.floor((PAWN_WIDTH + PAWN_HEIGHT) * 1.0205)
        for pawn in pawns_position:
            image = pygame.image.load(IMAGE_PATH)
            image = pygame.transform.scale(image, (PAWN_WIDTH, PAWN_HEIGHT))
            image_rect = image.get_rect()
            image_rect.topleft = (
                START_POSITION[0] + OFFSET * pawn["position"] + 2,
                START_POSITION[1] + OFFSET * (5 - pawn["number"]) + 3,
            )
            if pawn["return"] == True or pawn["position"] == 6:
                image = pygame.transform.rotate(image, 180)
            surface.blit(image, image_rect)
    elif player_number == 2:
        DIR_PATH = os.path.dirname(__file__)
        IMAGE_PATH = os.path.join(DIR_PATH, "..", "Assets", "Player2.png")
        PAWN_WIDTH = math.floor(game_width / 128)
        PAWN_HEIGHT = math.floor(game_width / 16)
        START_POSITION = (
            math.floor(game_width / 4 + 1.5 * PAWN_HEIGHT + 1.5 * PAWN_WIDTH) + 3,
            math.floor(game_height - PAWN_WIDTH) - 1,
        )
        OFFSET = math.floor((PAWN_WIDTH + PAWN_HEIGHT) * 1.0205)
        for pawn in pawns_position:
            image = pygame.image.load(IMAGE_PATH)
            image = pygame.transform.scale(image, (PAWN_WIDTH, PAWN_HEIGHT))
            image_rect = image.get_rect()
            image_rect.bottomleft = (
                START_POSITION[0] + OFFSET * (pawn["number"] - 1),
                START_POSITION[1] - OFFSET * pawn["position"],
            )
            if pawn["return"] == True or pawn["position"] == 6:
                image = pygame.transform.rotate(image, 180)
            surface.blit(image, image_rect)
