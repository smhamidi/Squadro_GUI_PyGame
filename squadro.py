import pygame
import math
from utils.components import create_main_board
from utils.components import place_player_pawns
from utils.components import draw_player_info_box_text
import json
import threading
import http.server
import socketserver
import requests
import os


pygame.init()

# GUI States
FONT_PATH = os.path.join("fonts", "RobotoMono.ttf")


# Finding the host display information
display_info = pygame.display.Info()
MAX_WIDTH = display_info.current_w
MAX_HEIGHT = display_info.current_h


# Setting the game display
pygame.display.set_caption("Squadro by smhamidi")
GAME_WIDTH = math.floor(MAX_WIDTH * 0.80)
GAME_HEIGHT = math.floor(GAME_WIDTH / 2)
DISPLAY = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
# --- Display Style
DISPLAY.fill((245, 245, 245))
print(GAME_WIDTH, GAME_HEIGHT)


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

# --- 1st Player states
PLAYER1_PAWNS = [
    {"number": 1, "position": 0, "return": False, "f_number": 1, "r_number": 3},
    {"number": 2, "position": 0, "return": False, "f_number": 3, "r_number": 1},
    {"number": 3, "position": 0, "return": False, "f_number": 2, "r_number": 2},
    {"number": 4, "position": 0, "return": False, "f_number": 3, "r_number": 1},
    {"number": 5, "position": 0, "return": False, "f_number": 1, "r_number": 3},
]
PLAYER1_COLOR = (184, 146, 48)
player1_ip = "127.0.0.1"
player1_port = 8081
player1_reply_port = 9081

# --- 2nd Player states
PLAYER2_PAWNS = [
    {"number": 1, "position": 0, "return": False, "f_number": 3, "r_number": 1},
    {"number": 2, "position": 0, "return": False, "f_number": 1, "r_number": 3},
    {"number": 3, "position": 0, "return": False, "f_number": 2, "r_number": 2},
    {"number": 4, "position": 0, "return": False, "f_number": 1, "r_number": 3},
    {"number": 5, "position": 0, "return": False, "f_number": 3, "r_number": 1},
]
PLAYER2_COLOR = (155, 28, 49)
player2_ip = "127.0.0.1"
player2_port = 8082
player2_reply_port = 9082

# --- Game states
running = True
current_player = 1


# Game Clock
FPS = 60
CLOCK = pygame.time.Clock()


# Game Functions
def process_move(move, player_id):
    global PLAYER1_PAWNS, PLAYER2_PAWNS

    try:
        pawn_number_to_move = int(move.get("move"))
    except (ValueError, TypeError):
        return False  # Invalid move format

    if not (1 <= pawn_number_to_move <= 5):
        return False  # Invalid pawn number

    if player_id == 1:
        current_player_pawns_list = PLAYER1_PAWNS
        opponent_player_pawns_list = PLAYER2_PAWNS
    elif player_id == 2:
        current_player_pawns_list = PLAYER2_PAWNS
        opponent_player_pawns_list = PLAYER1_PAWNS
    else:
        return False  # Invalid player_id

    moving_pawn_dict = current_player_pawns_list[pawn_number_to_move - 1]

    # Check if pawn has already finished its race
    if moving_pawn_dict["position"] == 0 and moving_pawn_dict["return"] == True:
        return False  # Cannot move a finished pawn

    start_pos = moving_pawn_dict["position"]
    is_returning = moving_pawn_dict["return"]
    current_pawn_track_id = moving_pawn_dict["number"]

    if not is_returning:  # Forward move
        strength = moving_pawn_dict["f_number"]
        direction = 1
    else:  # Return move
        strength = moving_pawn_dict["r_number"]
        direction = -1

    # Collision and Movement Logic

    # Calculate the pawn's intended destination if no jumps occur
    intended_pos_no_jumps = start_pos + direction * strength

    pos_after_initial_path_resolution = intended_pos_no_jumps

    # Find the *first* opponent encountered on the initial path segment (defined by 'strength')
    first_opponent_to_jump = None
    min_dist_to_first_opp = float("inf")  # Smallest distance to an opponent on the path

    for opp_pawn in opponent_player_pawns_list:
        # Skip opponent pawns that have finished their race
        if opp_pawn["position"] == 0 and opp_pawn["return"] == True:
            continue

        if opp_pawn["position"] == current_pawn_track_id:
            opp_coord_on_moving_pawns_axis = opp_pawn["number"]

            is_on_path = False
            if direction == 1:  # Moving forward (e.g., P1 from col 0 towards 6)
                # Opponent is on path if its coord is > start_pos and <= intended_pos_no_jumps
                if start_pos < opp_coord_on_moving_pawns_axis <= intended_pos_no_jumps:
                    is_on_path = True
            else:  # Moving backward (e.g., P1 from col 6 towards 0)
                # Opponent is on path if its coord is < start_pos and >= intended_pos_no_jumps
                if intended_pos_no_jumps <= opp_coord_on_moving_pawns_axis < start_pos:
                    is_on_path = True

            if is_on_path:
                dist = abs(opp_coord_on_moving_pawns_axis - start_pos)
                if dist < min_dist_to_first_opp:
                    min_dist_to_first_opp = dist
                    first_opponent_to_jump = opp_pawn
                # If multiple opponents are equidistant, this picks the one encountered first in the list.
                # Squadro rules might have specific tie-breakers (e.g., lower pawn number). Assuming any is fine.

    if first_opponent_to_jump:
        # A jump occurs. The moving pawn lands one step beyond this first opponent.
        jumped_opp = first_opponent_to_jump
        # The coordinate of jumped_opp on the moving pawn's axis was jumped_opp["number"]
        pos_after_initial_path_resolution = jumped_opp["number"] + direction

        # Reset jumped_opp to its last departing base
        if not jumped_opp["return"]:  # If opponent was on its forward journey
            jumped_opp["position"] = 0
        else:  # If opponent was on its return journey
            jumped_opp["position"] = 6
    # else: No jump on the initial path, pos_after_initial_path_resolution remains intended_pos_no_jumps

    # --- Chain Reaction Jumps
    final_effective_pos = pos_after_initial_path_resolution

    while True:
        opponent_at_landing_spot = None
        for opp_pawn_in_chain in opponent_player_pawns_list:
            # Skip finished opponent pawns
            if (
                opp_pawn_in_chain["position"] == 0
                and opp_pawn_in_chain["return"] == True
            ):
                continue

            # Check if this opponent is AT `final_effective_pos` on the current pawn's track
            if (
                opp_pawn_in_chain["position"] == current_pawn_track_id
                and opp_pawn_in_chain["number"] == final_effective_pos
            ):
                opponent_at_landing_spot = opp_pawn_in_chain
                break

        if opponent_at_landing_spot:
            # Jump this opponent in the chain
            jumped_opp_in_chain = opponent_at_landing_spot
            final_effective_pos += direction  # Moving pawn advances one more cell

            # Reset this newly jumped opponent to its last departing base
            if not jumped_opp_in_chain["return"]:
                jumped_opp_in_chain["position"] = 0
            else:
                jumped_opp_in_chain["position"] = 6
        else:
            # No opponent at the current landing spot, so the chain reaction ends
            break

    moving_pawn_dict["position"] = final_effective_pos
    # --- End Collision and Movement Logic

    # Boundary checks and updating 'return' status
    # (This part is similar to your original code, adapted for the new position)
    if not is_returning:  # Pawn was moving forward
        if moving_pawn_dict["position"] > 5:  # Reached or passed far side (position 6)
            moving_pawn_dict["position"] = 6
            moving_pawn_dict["return"] = True  # Pawn turns around
        elif (
            moving_pawn_dict["position"] < 0
        ):  # Jumped backward off the board (e.g. from pos 0, jumped something at pos -1 -> lands at -2)
            moving_pawn_dict["position"] = 0  # Cap at start position
            # 'return' status remains False as it hasn't completed a forward trip.

    elif is_returning:  # Pawn was moving backward (on its return trip)
        if (
            moving_pawn_dict["position"] < 1
        ):  # Reached or passed starting side (position 0)
            moving_pawn_dict["position"] = 0
            # 'return' is already True. Pawn is now finished (pos=0, return=True).
        elif (
            moving_pawn_dict["position"] > 6
        ):  # Jumped forward off the board while returning
            moving_pawn_dict["position"] = 6  # Cap at far end position
            # 'return' status remains True. Pawn is back at the far end.

    return True


class PlayerHandler(http.server.BaseHTTPRequestHandler):
    player_number = None
    next_player = None

    def do_POST(self):
        global current_player

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            move_data = json.loads(post_data.decode("utf-8"))

            # Only process if it's this player's turn
            if current_player == self.player_number:
                status = process_move(move_data, current_player)
                response = {"status": status}

                if status is True:
                    # Sending the move to the other player
                    if current_player == 1:
                        ip, port = player2_ip, player2_reply_port
                    else:
                        ip, port = player1_ip, player1_reply_port

                    url = f"http://{ip}:{port}"
                    try:
                        requests.post(
                            url,
                            json={"player": current_player, "move": move_data["move"]},
                            timeout=1,
                        )
                    except requests.exceptions.RequestException as exc:
                        print(
                            f"[ERROR] Could not notify player {self.next_player}: {exc}"
                        )

                    # Switch to the next player's turn
                    current_player = self.next_player
                else:
                    raise Exception(f"Invalid Move: {move_data}")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Not your turn"}).encode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress log messages to keep console clean
        return


class Player1Handler(PlayerHandler):
    player_number = 1
    next_player = 2


class Player2Handler(PlayerHandler):
    player_number = 2
    next_player = 1


# Start the HTTP servers
def start_servers():
    # Create server for Player 1
    player1_server = socketserver.TCPServer(("127.0.0.1", player1_port), Player1Handler)
    player1_thread = threading.Thread(target=player1_server.serve_forever)
    player1_thread.daemon = True
    player1_thread.start()
    print(f"Player 1 server started at {"127.0.0.1"}:{player1_port}")

    # Create server for Player 2
    player2_server = socketserver.TCPServer(("127.0.0.1", player2_port), Player2Handler)
    player2_thread = threading.Thread(target=player2_server.serve_forever)
    player2_thread.daemon = True
    player2_thread.start()
    print(f"Player 2 server started at {"127.0.0.1"}:{player2_port}")


# Start the servers before the game loop
start_servers()


# Main Game Loop
while running:
    # Clicking exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game Board
    MAIN_BOARD = pygame.Surface((GAME_HEIGHT, GAME_HEIGHT))
    MAIN_BOARD.fill((34, 34, 34))
    MAIN_BOARD = create_main_board(
        MAIN_BOARD, GAME_HEIGHT, GAME_HEIGHT, PLAYER1_PAWNS, PLAYER2_PAWNS
    )
    # --- Positioning the Board
    MAIN_BOARD_RECT = MAIN_BOARD.get_rect()
    MAIN_BOARD_RECT.topleft = (GAME_HEIGHT // 2, 0)
    DISPLAY.blit(MAIN_BOARD, MAIN_BOARD_RECT)

    # Players info box rects - highlight current player
    player1_box_color = PLAYER1_COLOR if current_player == 1 else (0, 0, 0)
    player2_box_color = PLAYER2_COLOR if current_player == 2 else (0, 0, 0)

    # Players info box rects
    pygame.draw.rect(
        DISPLAY,
        player1_box_color,
        PLAYER1_BOX,
        border_radius=INFOBOX_RADIUS,
        width=INFOBOX_THICKNESS,
    )
    pygame.draw.rect(
        DISPLAY,
        player2_box_color,
        PLAYER2_BOX,
        border_radius=INFOBOX_RADIUS,
        width=INFOBOX_THICKNESS,
    )

    draw_player_info_box_text(
        DISPLAY,
        1,
        player1_ip,
        player1_port,
        player1_reply_port,
        PLAYER1_BOX,
        FONT_PATH,
    )

    draw_player_info_box_text(
        DISPLAY,
        2,
        player2_ip,
        player2_port,
        player2_reply_port,
        PLAYER2_BOX,
        FONT_PATH,
    )

    # Updating the display
    pygame.display.update()

    # Using Clock for ensuring 60fps
    CLOCK.tick(FPS)

# Quit pygame
pygame.quit()
