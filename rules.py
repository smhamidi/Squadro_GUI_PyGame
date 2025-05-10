# Game states (assuming these are globally accessible as in your example)

# --- 1st Player states
PLAYER1_PAWNS = [
    {"number": 1, "position": 0, "return": False, "f_number": 1, "r_number": 3},
    {"number": 2, "position": 0, "return": False, "f_number": 3, "r_number": 1},
    {"number": 3, "position": 0, "return": False, "f_number": 2, "r_number": 2},
    {"number": 4, "position": 0, "return": False, "f_number": 3, "r_number": 1},
    {"number": 5, "position": 0, "return": False, "f_number": 1, "r_number": 3},
]

# --- 2nd Player states
PLAYER2_PAWNS = [
    {
        "number": 1,
        "position": 0,
        "return": False,
        "f_number": 3,
        "r_number": 1,
    },  # Corresponds to column 1 for P2
    {
        "number": 2,
        "position": 0,
        "return": False,
        "f_number": 1,
        "r_number": 3,
    },  # Corresponds to column 2 for P2
    {
        "number": 3,
        "position": 0,
        "return": False,
        "f_number": 2,
        "r_number": 2,
    },  # Corresponds to column 3 for P2
    {
        "number": 4,
        "position": 0,
        "return": False,
        "f_number": 1,
        "r_number": 3,
    },  # Corresponds to column 4 for P2
    {
        "number": 5,
        "position": 0,
        "return": False,
        "f_number": 3,
        "r_number": 1,
    },  # Corresponds to column 5 for P2
]


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

    # Get the specific pawn object. Assumes pawns are ordered by 'number' in the list.
    # (pawn_number_to_move is 1-5, list index is 0-4)
    moving_pawn_dict = current_player_pawns_list[pawn_number_to_move - 1]

    # Sanity check if the pawn's number field matches (optional but good practice)
    if moving_pawn_dict["number"] != pawn_number_to_move:
        # This indicates an issue with pawn list structure or assumptions.
        # For now, we trust the indexing.
        print(f"Warning: Mismatch for player {player_id}, pawn {pawn_number_to_move}.")

    # Check if pawn has already finished its race
    # A pawn is finished if it's at position 0 AND on its return trip.
    if moving_pawn_dict["position"] == 0 and moving_pawn_dict["return"] == True:
        return False  # Cannot move a finished pawn

    start_pos = moving_pawn_dict["position"]
    is_returning = moving_pawn_dict["return"]
    # current_pawn_track is the 'lane' number (row for P1, column for P2)
    # This is used to identify if an opponent pawn is on the same geometric line.
    current_pawn_track_id = moving_pawn_dict["number"]

    if not is_returning:  # Forward move
        strength = moving_pawn_dict["f_number"]
        direction = 1
    else:  # Return move
        strength = moving_pawn_dict["r_number"]
        direction = -1

    # --- Collision and Movement Logic ---

    # Calculate the pawn's intended destination if no jumps occur
    intended_pos_no_jumps = start_pos + direction * strength

    # This variable will hold the pawn's position after the initial part of the move (either normal advance or first jump)
    pos_after_initial_path_resolution = intended_pos_no_jumps

    # Find the *first* opponent encountered on the initial path segment (defined by 'strength')
    first_opponent_to_jump = None
    min_dist_to_first_opp = float("inf")  # Smallest distance to an opponent on the path

    for opp_pawn in opponent_player_pawns_list:
        # Skip opponent pawns that have finished their race
        if opp_pawn["position"] == 0 and opp_pawn["return"] == True:
            continue

        # An opponent pawn is on the moving pawn's line of movement if:
        #   - P1 moving (along a row): Opponent P2's current row (`opp_pawn["position"]`) matches P1's row (`current_pawn_track_id`).
        #   - P2 moving (along a col): Opponent P1's current col (`opp_pawn["position"]`) matches P2's col (`current_pawn_track_id`).
        # This translates to: `opp_pawn["position"] == current_pawn_track_id`

        # The opponent's coordinate *along the moving pawn's axis of movement* is `opp_pawn["number"]`.
        #   - P1 moving (cols 0-6): P2's relevant coordinate is its column number (`opp_pawn["number"]`).
        #   - P2 moving (rows 0-6): P1's relevant coordinate is its row number (`opp_pawn["number"]`).
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

    # --- Chain Reaction Jumps ---
    # The pawn has landed at `pos_after_initial_path_resolution`.
    # Check if this landing spot is occupied by another opponent.
    # `final_effective_pos` starts as the landing spot from the first phase.
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
    # --- End Collision and Movement Logic ---

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
