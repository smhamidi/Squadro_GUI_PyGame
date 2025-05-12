import pygame
import math
import os


def create_main_board(
    surface, surface_width, surface_height, player1_pawn, player2_pawn
):
    draw_start_lines(surface, surface_width, surface_height)
    place_base_pawns(surface, surface_width, surface_height)

    DIR_PATH = os.path.dirname(__file__)
    CROSS_IMG = pygame.image.load(os.path.join(DIR_PATH, "..", "assets", "Cross.png"))
    CROSS_IMG = pygame.transform.scale(
        CROSS_IMG, (surface_height // 8, surface_height // 8)
    )
    SMALL_OFFSET = surface_height // 64
    BIG_OFFSET = surface_height // 8
    START_TOP_LEFT = (2 * SMALL_OFFSET + BIG_OFFSET, 2 * SMALL_OFFSET + BIG_OFFSET)
    for i in range(5):
        for j in range(5):
            CROSS_RECT = (
                START_TOP_LEFT[0] + j * BIG_OFFSET + j * SMALL_OFFSET,
                START_TOP_LEFT[1] + i * BIG_OFFSET + i * SMALL_OFFSET,
            )
            surface.blit(CROSS_IMG, CROSS_RECT)

    place_player_pawns(1, player1_pawn, surface, surface_width, surface_height)
    place_player_pawns(2, player2_pawn, surface, surface_width, surface_height)

    return surface


import os
import math
import pygame


def place_base_pawns(surface, surface_width, surface_height):
    # --- Offsets
    small_off = surface_height // 64
    big_off = surface_height // 8
    offset = small_off + big_off

    # --- Load & scale bases
    dir_path = os.path.dirname(__file__)
    assets = os.path.join(dir_path, "..", "assets")
    names = ["Base1.png", "Base2.png", "Base3.png"]

    # load original
    bases = [pygame.image.load(os.path.join(assets, name)) for name in names]

    # compute target size
    init_w, init_h = bases[0].get_size()
    des_h = surface_height // 8
    des_w = int(des_h * (init_w / init_h))

    scaled = [pygame.transform.scale(b, (des_w, des_h)) for b in bases]

    # --- Precompute common geometry
    circle_w = (des_w - small_off) / 2
    start_off = math.floor(1.5 * offset) - circle_w

    # --- Per-side configuration
    config = {
        "UP": {"angle": 0, "sequence": [0, 2, 1, 2, 0], "row_delta": 0},
        "DOWN": {"angle": 180, "sequence": [2, 0, 1, 0, 2], "row_delta": 6 * offset},
        "RIGHT": {"angle": 270, "sequence": [2, 0, 1, 0, 2], "col_delta": 6 * offset},
        "LEFT": {"angle": 90, "sequence": [0, 2, 1, 2, 0], "col_delta": 0},
    }

    # --- Blit them all
    for side, cfg in config.items():
        # rotate each base to this side's orientation
        rotated = [pygame.transform.rotate(img, cfg["angle"]) for img in scaled]

        if side in ("UP", "DOWN"):
            y = small_off + cfg["row_delta"]
            for i, idx in enumerate(cfg["sequence"]):
                x = int(start_off + i * offset)
                surface.blit(rotated[idx], (x, int(y)))

        else:  # RIGHT or LEFT
            x = small_off + cfg["col_delta"]
            for i, idx in enumerate(cfg["sequence"]):
                y = int(start_off + i * offset)
                surface.blit(rotated[idx], (int(x), y))


def draw_start_lines(surface, surface_width, surface_height):
    SMALL_OFFSET = surface_height // 64
    BIG_OFFSET = surface_height // 8
    OFFSET = SMALL_OFFSET + BIG_OFFSET
    pygame.draw.line(
        surface,
        (245, 245, 245),
        (BIG_OFFSET - SMALL_OFFSET, OFFSET + SMALL_OFFSET),
        (BIG_OFFSET - SMALL_OFFSET, 6 * OFFSET),
        width=SMALL_OFFSET // 2,
    )

    pygame.draw.line(
        surface,
        (245, 245, 245),
        (OFFSET + SMALL_OFFSET, 6 * OFFSET + 3 * SMALL_OFFSET),
        (6 * OFFSET, 6 * OFFSET + 3 * SMALL_OFFSET),
        width=SMALL_OFFSET // 2,
    )


def place_player_pawns(
    player_number, pawns_position, surface, surface_width, surface_height
):
    SMALL_OFFSET = surface_height // 64
    BIG_OFFSET = surface_height // 8
    if player_number == 1:
        DIR_PATH = os.path.dirname(__file__)
        IMAGE_PATH = os.path.join(DIR_PATH, "..", "assets", "Player1.png")
        START_POSITION = (
            SMALL_OFFSET,
            math.floor(1.5 * BIG_OFFSET + 1.5 * SMALL_OFFSET),
        )
        OFFSET = BIG_OFFSET + SMALL_OFFSET
        for pawn in pawns_position:
            if pawn["position"] == 0 and pawn["return"] == True:
                continue
            image = pygame.image.load(IMAGE_PATH)
            image = pygame.transform.scale(image, (BIG_OFFSET, SMALL_OFFSET))
            image_rect = image.get_rect()
            image_rect.topleft = (
                START_POSITION[0] + OFFSET * pawn["position"],
                START_POSITION[1] + OFFSET * (5 - pawn["number"]),
            )
            if pawn["return"] == True or pawn["position"] == 6:
                image = pygame.transform.rotate(image, 180)
            surface.blit(image, image_rect)
    elif player_number == 2:
        DIR_PATH = os.path.dirname(__file__)
        IMAGE_PATH = os.path.join(DIR_PATH, "..", "Assets", "Player2.png")
        OFFSET = BIG_OFFSET + SMALL_OFFSET
        START_POSITION = (
            math.floor(1.5 * OFFSET),
            6 * OFFSET + SMALL_OFFSET,
        )
        for pawn in pawns_position:
            if pawn["position"] == 0 and pawn["return"] == True:
                continue
            image = pygame.image.load(IMAGE_PATH)
            image = pygame.transform.scale(image, (SMALL_OFFSET, BIG_OFFSET))
            image_rect = image.get_rect()
            image_rect.topleft = (
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
    GAP_TITLE_INFO = 20  # Vertical gap between the title and the first info line
    GAP_BETWEEN_INFO_LINES = 8  # Extra vertical gap between each info line

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
