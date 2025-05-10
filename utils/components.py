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
            if pawn["position"] == 0 and pawn["return"] == True:
                continue
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
            if pawn["position"] == 0 and pawn["return"] == True:
                continue
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


def draw_player_info_box_text(
    surface, player_num, ip, port, reply_port, box_rect, font_path
):
    TITLE_FONT = pygame.font.Font(font_path, 30)
    INFO_FONT = pygame.font.Font(font_path, 22)
    TEXT_COLOR = (0, 0, 0)
    # Constants for padding and spacing inside the box
    PADDING_TOP = 10  # Padding from the top of the box to the title
    PADDING_HORIZONTAL_INFO = (
        15  # Horizontal padding for info text from the box's left edge
    )
    GAP_TITLE_INFO = 8  # Vertical gap between the title and the first info line
    GAP_BETWEEN_INFO_LINES = 4  # Extra vertical gap between each info line

    # 1. Render and position Title (e.g., "Player 1")
    title_text = f"Player {player_num}"
    title_surf = TITLE_FONT.render(title_text, True, TEXT_COLOR)
    title_rect = title_surf.get_rect()
    title_rect.centerx = box_rect.centerx  # Center horizontally in the box
    title_rect.top = box_rect.top + PADDING_TOP
    surface.blit(title_surf, title_rect)

    # Calculate starting Y position for the first info line (IP address)
    current_y = title_rect.bottom + GAP_TITLE_INFO
    info_line_height = (
        INFO_FONT.get_linesize()
    )  # Gets the recommended height for a line of text

    # 2. Render and position IP Address
    ip_text = f"IP: {ip}"
    ip_surf = INFO_FONT.render(ip_text, True, TEXT_COLOR)
    ip_rect = ip_surf.get_rect()
    ip_rect.left = box_rect.left + PADDING_HORIZONTAL_INFO
    ip_rect.top = current_y
    surface.blit(ip_surf, ip_rect)
    current_y += info_line_height + GAP_BETWEEN_INFO_LINES  # Move Y for the next line

    # 3. Render and position Port
    port_text = f"Port: {port}"
    port_surf = INFO_FONT.render(port_text, True, TEXT_COLOR)
    port_rect = port_surf.get_rect()
    port_rect.left = box_rect.left + PADDING_HORIZONTAL_INFO
    port_rect.top = current_y
    surface.blit(port_surf, port_rect)
    current_y += info_line_height + GAP_BETWEEN_INFO_LINES  # Move Y for the next line

    # 4. Render and position Reply Port
    reply_port_text = f"Reply Port: {reply_port}"
    reply_port_surf = INFO_FONT.render(reply_port_text, True, TEXT_COLOR)
    reply_port_rect = reply_port_surf.get_rect()
    reply_port_rect.left = box_rect.left + PADDING_HORIZONTAL_INFO
    reply_port_rect.top = current_y
    surface.blit(reply_port_surf, reply_port_rect)
