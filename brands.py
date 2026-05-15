## Terrible Python code, go! ##

#### Functions ####

# Rock value: no rock, yes rock, no rock button, yes rock button, hands (hands!)
# Beaver value: not present, down, left, up, right (charging store somewhere else?)
# Player value: not present, down, left, up, right
# Land value: hole, walkable, glass, stairs, wall

## Prints a brand in a readable way.
def display_brane(brane):
    if len(brane) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane)))

    string = ""
    for i in range(36):
        if brane[i] == 0:
            string += "_"
        elif brane[i] == 1:
            string += "█"
        elif brane[i] == 2:
            string += "/"
        elif brane[i] == 3:
            string += "S"
        elif brane[i] == 4:
            string += "W"
        elif get_player_value_from_tile(brane[i]) == 1:
            string += "V"
        elif get_player_value_from_tile(brane[i]) == 2:
            string += "<"
        elif get_player_value_from_tile(brane[i]) == 3:
            string += "^"
        elif get_player_value_from_tile(brane[i]) == 4:
            string += ">"
        else:
            string += "X"

        string += " "

        if i == 5 or i == 11 or i == 17 or i == 23 or i == 29:
            string += "\n"

    return string

## Given a player value and a land value, returns the appropriate tile value.
def create_tile_data(rock, beaver, player, land):
    if player > 4 or land > 4 or player < 0 or land < 0:
        error = input("Error! Invalid inputs in create_tile_data()! " + str(player) + " " + str(land))

    # return (5^2)*beaver + (5^1)*player + (5^0)*land
    return 125 * rock + 25 * beaver + 5 * player + land

## Given a tile value, extracts the rock value.
def get_rock_value_from_tile(x):
    return int(x / 125)

## Given a tile value, extracts the beaver value.
def get_beaver_value_from_tile(x):
    while x >= 125:
        x -= 125
    return int(x / 25)

## Given a tile value, extracts the player value.
def get_player_value_from_tile(x):
    while x >= 125:
        x -= 125
    while x >= 25:
        x -= 25
    return int(x / 5)

## Given a tile value, extracts the land value.
def get_land_value_from_tile(x):
    while x >= 125:
        x -= 125
    while x >= 25:
        x -= 25
    while x >= 5:
        x -= 5
    return x

    error = input("Error! Invalid input in get_land_value_from_tile()! " + str(x))

## Given a brane state and a brand, returns true if the brand is currently successfully carved.
def is_brand_carved(brane_state, brand):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(4, 4, 4, 4):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if i_brane_state_land == 0 and brand[i] == 0:
            continue
        elif i_brane_state_land != 0 and i_brane_state_land != 3 and brand[i] == 1:
            continue
        return False

    return True
    
## Given a brane state and a brand, returns true if the brand is currently successfully carved, ignoring stairs.
def is_brand_carved_minus_stairs(brane_state, brand):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(4, 4, 4, 4):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if i_brane_state_land == 0 and brand[i] == 0:
            continue
        elif i_brane_state_land == 3 and brand[i] == 0:
            continue
        elif i_brane_state_land != 0 and brand[i] == 1:
            continue
        return False

    return True
    
## Given a brane state and a brand, returns true if the brand would be successfully carved if the tile the player is currently standing on is glass and was removed.
def is_brand_carved_minus_stood_glass(brane_state, brand):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(4, 4, 4, 4):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if i_brane_state_land == 0 and brand[i] == 0:
            continue
        elif i_brane_state_land != 0 and i_brane_state_land != 3 and brand[i] == 1:
            continue
        elif i_brane_state_land == 2 and get_player_value_from_tile(brane_state[i]) > 0 and brand[i] == 0:
            continue
        return False

    return True

## Given a brane state, returns the index of the player's position.
def get_player_index(brane_state):
    store = -1
    for i in range(36):
        if get_player_value_from_tile(brane_state[i]) > 0:
            if store != -1:
                error = input("Error! Multiple players found by get_player_index()! "+ display_brane(brane_state))

            store = i

    if store != -1:
        return store

    error = input("Error! Player could not be found by get_player_index()! "+ display_brane(brane_state))

## Given a brane state, returns the index of the stairs.
def get_stairs_index(brane_state):
    store = -1
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == 3:
            if store != -1:
                error = input("Error! Multiple stairs found by get_stairs_index()! "+ display_brane(brane_state))

            store = i

    if store != -1:
        return store

    error = input("Error! Stairs could not be found by get_stairs_index()! "+ display_brane(brane_state))

## Given a brane state, returns the land value of the tile the player is standing on.
def get_player_land_value(brane_state):
    return get_land_value_from_tile(brane_state[get_player_index(brane_state)])

## Given a brane state, returns the player's facing value.
def get_player_direction(brane_state):
    return get_player_value_from_tile(brane_state[get_player_index(brane_state)])

## Given a brane state, returns the player's facing value as a letter.
def player_faced_direction_letter(brane_state):
    return ["D", "L", "U", "R"][get_player_direction(brane_state) - 1]

## Given a facing letter, returns the equivalent number.
def direction_letter_to_number(letter):
    if letter == "D":
        return 1
    elif letter == "L":
        return 2
    elif letter == "U":
        return 3
    elif letter == "R":
        return 4
    else:
        error = input("Error! No valid number equivalent for letter input in direction_letter_to_number()! " + letter)

## Gives the tile INDEX of the tile in front of the player. Don't call this directly unless handling -1 case.
## Direction provided can be either integer or letter.
def index_tile_in_direction_of_player(brane_state, player_direction=-1):
    player_i = get_player_index(brane_state)
    if player_direction == -1:
        player_direction = get_player_value_from_tile(brane_state[player_i])

    if player_direction == 0:
        error = input("Error! Player does not exist to index_tile_in_front_of_player()!")
    elif player_direction == 1 or player_direction == "D":  # down
        if player_i + 6 > 35:
            return -1
        else:
            return player_i + 6
    elif player_direction == 2 or player_direction == "L":  # left
        if (player_i == 0 or player_i == 6 or player_i == 12 or player_i == 18 or player_i == 24 or player_i == 30):
            return -1
        else:
            return player_i - 1
    elif player_direction == 3 or player_direction == "U":  # up
        if player_i - 6 < 0:
            return -1
        else:
            return player_i - 6
    elif player_direction == 4 or player_direction == "R":  # right
        if (player_i == 5 or player_i == 11 or player_i == 17 or player_i == 23 or player_i == 29 or player_i == 35):
            return -1
        else:
            return player_i + 1
    else:
        error = input("Error! Player does not have valid direction to index_tile_in_direction_of_player()! "+brane_state)

## Same as the above but returns the actual data in one step.
def tile_in_direction_of_player(brane_state, forced_direction=-1):
    i = index_tile_in_direction_of_player(brane_state, forced_direction)

    if i == -1:
        return 4
    else:
        return brane_state[i]

## Returns true if the void rod can take a file.
def void_rod_can_take():
    return len(held_tile) == 0 or endless

## Given a direction as a letter, returns the opposite direction.
def opposite_direction_letter(letter):
    if letter == "U":
        return "D"
    elif letter == "D":
        return "U"
    elif letter == "L":
        return "R"
    elif letter == "R":
        return "L"
    else:
        return "X"

## Returns true if there any MOVING monsters in the brane. Because this is used to deterime if turn-wasting is worthwhile, hands (hands!) are not counted.
def here_be_monsters_question(brane_state):
    for i in range(36):
        if get_beaver_value_from_tile(brane_state[i]) != 0:
            return True

    return False

## Returns true if the input brane state has any glass in it.
def brane_has_glass_question(brane_state):
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == 2:
            return True
    return False

## Returns true if the input brane state has an exit.
def brane_has_stairs_question(brane_state):
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == 3:
            return True
    return False

## Counts brand-valid tiles.
def count_solids(brane_state):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    counter = 0
    for i in range(36):
        if (get_land_value_from_tile(brane_state[i]) != 0 and get_land_value_from_tile(brane_state[i]) != 3):
            counter += 1
        elif brane_state[i] != 0 and brane_state[i] != 3:
            print(brane_state[i])
    return counter

## Counts state-1 tiles.
def count_true_solids(brane_state):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    counter = 0
    for i in range(36):
        if (get_land_value_from_tile(brane_state[i]) == 1):
            counter += 1
    return counter

## Checks if the stairs are active (i.e., available to exit from)
def stairs_exitable_question(brane_state):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    for i in range(36):
        # no rock, yes rock, no rock button, yes rock button, hands (hands!)
        if get_rock_value_from_tile(brane_state[i]) == 2:
            return False

    return True

## Returns the number of valid tiles currently held by the wand.
def held_valids():
    counter = 0
    for x in held_tile:
        if x != 0 and x != 3:
            counter += 1
    return counter
    
## Gives a value representing the "distance" between a brane state and the solution.
def distance_from_heaven(brane_state, brand):
    distance = 0
    
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        
        if i_brane_state_land == 0 and brand[i] == 0:
            continue
        elif (i_brane_state_land == 1 or i_brane_state_land == 2 or i_brane_state_land == 4) and brand[i] == 1:
            continue
        
        distance += 1
    
    return distance
    
## Returns taxicab distance between two points on the brane room, given by their index.
def taxicab_distance(a,b):
    x1 = a % 6
    y1 = int(a/6)
    
    x2 = b % 6
    y2 = int(b/6)
    
    return abs(x1 - x2) + abs(y1 - y2)
    
## Returns True if the tile is undesireable (or impossible) to move into. Take a land value.
def land_undesirable(land, brane_state):
    return land == 0 or land == 4 or (land == 3 and stairs_exitable_question(brane_state))
    
## Given the state and an input, returns the predicted change in "solution distance" if the player were to take that action.
## Positive change indicates increasing distance, while negative represents lowering the distance. Thus, here, negative is desirable.
def predicted_distance_change(brane_state, input_letter):
    total = 0
    
    brand = brand_dicts[chosen_brand]
    
    faced_tile = tile_in_direction_of_player(brane_state)
    faced_tile_land_value = get_land_value_from_tile(faced_tile)
    
    if input_letter == "Z":
        # Player is placing a tile.
        if faced_tile_land_value == 0 and len(held_tile) != 0:
            # Player is placing stairs.
            if held_tile[-1] == 3:
                total += 1
            # Player is placing a tile where the brand has a solid tile.
            elif brand[index_tile_in_direction_of_player(brane_state)] == 1:
                total += -1
            # Player is placing a tile where the brand does NOT have a solid tile.
            else:
                total += 1
        # Player is picking up a tile.
        elif faced_tile_land_value != 0 and faced_tile_land_value != 4 and void_rod_can_take():
            # Player is picking up stairs.
            if faced_tile_land_value == 3:
                total += -1
            # Player is picking up a tile where the brand has an empty tile.
            elif brand[index_tile_in_direction_of_player(brane_state)] == 0:
                total += -1
            else:
                total += 1
    elif input_letter == "D" or input_letter == "L" or input_letter == "U" or input_letter == "R":
        # Standing on glass.
        if get_player_land_value(brane_state) == 2:
            # Tile we're moving into is glass, dooming BOTH our tiles.
            if faced_tile_land_value == 2:
                if brand[get_player_index(brane_state)] == 0:
                    total += -1
                else:
                    total += 1
                if brand[index_tile_in_direction_of_player(brane_state)] == 0:
                    total += -1
                else:
                    total += 1
            # Tile we're moving into is moveinto-able, but not glass
            elif not (faced_tile_land_value == 3 and stairs_exitable_question(brane_state)) and faced_tile_land_value != 4:
                # Determine the effect of this action.
                if brand[get_player_index(brane_state)] == 0:
                    total += -1
                else:
                    total += 1
        # Moving into glass
        elif faced_tile_land_value == 2:
            if brand[index_tile_in_direction_of_player(brane_state)] == 0:
                total += -1
            else:
                total += 1
                    
        # Fractional weights for moving closer to the stairs.
        if brane_has_stairs_question(brane_state):
            total += (taxicab_distance(index_tile_in_direction_of_player(brane_state),get_stairs_index(brane_state)) - taxicab_distance(get_player_index(brane_state),get_stairs_index(brane_state))) / 3
    
    # Failsafe: distance is 0.
    return total
    
## Based on brane state and choice, returns the threshold based on its prediction.
def threshold_from_choice(current_brane_layout,choice):
    # \min\left(0.95,\max\left(0.05,0.5\cdot\frac{\left(x+1.5\right)}{\left(1.5\right)}\right)\right)
    
    slant_factor = 100
    threshold = 0.5*((predicted_distance_change(current_brane_layout,choice)+slant_factor)/slant_factor)
    
    # Clamp the threshold so that nothing is ever truly certain or impossible
    if threshold > 0.95:
        threshold = 0.95
    elif threshold < 0.05:
        threshold = 0.05
        
    return threshold
    
## Given an i value for a brane array and movements on the x and y axis, returns a new i index cooresponding to that movement.
def move_cartesian(i, x, y):
    store = i + x + 6*y
    
    if store > 35 or store < 0 or int(i/6) != int ((i+x)/6):
        return -1
    else:
        return store
    
## Given a starting position and cartesian movements, returns the land value of the tile at that index. Accounts for OOB searching.
def land_at_moved_cartesian(i, brane_state, x, y):
    store = move_cartesian(i, x, y)
    
    if store == -1:
        return 4
    else:
        return get_land_value_from_tile(brane_state[store])
    
## Returns true if the land value of this tile is 1 or 3, inactive.
def effective_type_1(i, brane_state):
    return (get_land_value_from_tile(i) == 1 or (get_land_value_from_tile(i) == 3 and not stairs_exitable_question(brane_state))) and get_beaver_value_from_tile(i) == 0 and (get_rock_value_from_tile(i) == 0 or get_rock_value_from_tile(i) == 2)
    
## Returns true if there is a 3 line of moveable land tiles. This includes only type-1 and inactive type-3.
def three_line_present_strict(brane_state):
    for i in range(36):
        
        if i + 3 <= 35 and int(i/6) == int((i+3)/6) and effective_type_1(brane_state[i],brane_state) and effective_type_1(brane_state[i+1],brane_state) and effective_type_1(brane_state[i+2],brane_state):
            return True
        if i + 6*2 <= 35 and effective_type_1(brane_state[i],brane_state) and effective_type_1(brane_state[i+6],brane_state) and effective_type_1(brane_state[i+12],brane_state):
            return True
            
    return False
    
## Given a brane layout, returns the list of not-obviously-stupid inputs.
def safe_choice_list(brane_state, stupid_flaggot = False):
    choices = {"D", "L", "U", "R", "Z"}

    down_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 1))
    left_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 2))
    up_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 3))
    right_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 4))

    faced_tile = tile_in_direction_of_player(brane_state)
    faced_tile_land_value = get_land_value_from_tile(faced_tile)

    ## Deadly or round-ending ##
    ## Going down stairs or a pit (as shown by human-found optimal Eus solution, falling into a pit can be the requisite final step with glass)
    if (down_tile_land_value == 0 and not is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand])) or (down_tile_land_value == 3 and stairs_exitable_question(brane_state)):
        choices.remove("D")
    if (left_tile_land_value == 0 and not is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand])) or (left_tile_land_value == 3 and stairs_exitable_question(brane_state)):
        choices.remove("L")
    if (up_tile_land_value == 0 and not is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand])) or (up_tile_land_value == 3 and stairs_exitable_question(brane_state)):
        choices.remove("U")
    if (right_tile_land_value == 0 and not is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand])) or (right_tile_land_value == 3 and stairs_exitable_question(brane_state)):
        choices.remove("R")
        
    ## Breaking a piece of glass that brings total carve-valid tiles below the brand's amount.
    if "D" in choices and down_tile_land_value == 2 and count_solids(brane_state)+held_valids() == count_solids(brand_dicts[chosen_brand]):
        choices.remove("D")
    if "L" in choices and left_tile_land_value == 2 and count_solids(brane_state)+held_valids() == count_solids(brand_dicts[chosen_brand]):
        choices.remove("L")
    if "U" in choices and up_tile_land_value == 2 and count_solids(brane_state)+held_valids() == count_solids(brand_dicts[chosen_brand]):
        choices.remove("U")
    if "R" in choices and right_tile_land_value == 2 and count_solids(brane_state)+held_valids() == count_solids(brand_dicts[chosen_brand]):
        choices.remove("R")

    ## Dumb but not deadly ##
    ## There is no tile in front of the player and the player does not have any tile stored. There is no point in pressing "Z"
    if faced_tile_land_value == 0 and len(held_tile) == 0:
        choices.remove("Z")
    ## There is a tile in front of the player and the player lacks the ability to take it. There is no point in pressing "Z"
    elif faced_tile_land_value != 0 and not void_rod_can_take():
        choices.remove("Z")

    ## The tile in front is a wall, and there are no monsters to make wasting a turn meaningful.
    ## Hitting a wall to your side CAN be useful to reposition, so we will not discount it!
    if faced_tile_land_value == 4 and not here_be_monsters_question(brane_state) and player_faced_direction_letter(brane_state) in choices:
        choices.remove(player_faced_direction_letter(brane_state))

    ## Pointless movements (repetitive ones are trimmed afterward, not outright removed) ##
    if not here_be_monsters_question(brane_state):
        # Entering a dead end. (Smart bun.)
        #if get_player_land_value(brane_state) != 2:
        
        # Entering a dead end. (Dumb bun.)
        if get_player_land_value(brane_state) != 2:
            player_index = get_player_index(brane_state)
            cardinals = ["D","L","U","R"]
            
            for x in range(4):
                # Don't check to see if the land is moveable; if it hasn't been removed by an earlier filter, it is.
                if cardinals[x] not in choices:
                    continue
                
                # Confirm potential movement tile attributes and make pawn tile variables.
                if x == 0 and down_tile_land_value != 2 and not land_undesirable(down_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,2)
                elif x == 1 and left_tile_land_value != 2 and not land_undesirable(left_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,-2,0)
                elif x == 2 and up_tile_land_value != 2 and not land_undesirable(up_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,-2)
                elif x == 3 and right_tile_land_value != 2 and not land_undesirable(right_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,2,0)
                else:
                    continue
                
                pawn_land_value_backwards = get_land_value_from_tile(tile_in_direction_of_player(brane_state,opposite_direction_letter(cardinals[x])))
                
                # Ignore if at the end of the "dead end" we could potentially place or pick up a tile. That makes it useful.
                if (pawn_land_value_first_turn == 0 and len(held_tile) > 0) or (pawn_land_value_first_turn != 0 and pawn_land_value_first_turn != 4 and void_rod_can_take()):
                    pass
                # Ignore if the tile behind the player is solid, or empty and the void rod can place. This could be a useful repositioning tactic.
                elif (pawn_land_value_backwards == 0 and len(held_tile) > 0) or pawn_land_value_backwards == 1 or pawn_land_value_backwards == 2 or (pawn_land_value_backwards == 3 and not stairs_exitable_question(brane_state)):
                    pass
                # Remove if dead end.
                elif land_undesirable(pawn_land_value_attack_1, brane_state) and land_undesirable(pawn_land_value_attack_2, brane_state) and land_undesirable(pawn_land_value_first_turn, brane_state):
                    print("Pawn values found to be dead end:",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    print("Direction:",cardinals[x])
                    choices.remove(cardinals[x])
                else:
                    pass
                    #print("Pawn values found not to be dead end:",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    #print("Direction:",cardinals[x])
    
    if not here_be_monsters_question(brane_state) and "Z" in choices:
        # Double z's are never useful without monsters
        if len(working_moves) > 0 and working_moves[-1] == "Z":
            choices.remove("Z")
        # Trapping yourself is never worth it. (The "final stairs" case is overriden in a later block, disregard.)
        elif not wings and void_rod_can_take() and faced_tile_land_value != 0 and brane_has_stairs_question(brane_state) and int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state)) == 3:
            choices.remove("Z")
    
    ## Historically bad choices ##
    for choice in {"D","L","U","R","Z"}:
        if (working_moves + [choice]) in bad_solutions and choice in choices:
            choices.remove(choice)
            
    ## Obviously correct choices ##
    # If removing the stairs is the last step and we're already facing them, always do that.
    if is_brand_carved_minus_stairs(brane_state, brand_dicts[chosen_brand]) and faced_tile_land_value == 3 and void_rod_can_take():
        choices = {"Z"}
        
    # If breaking the glass we're currently on is the last step, always do that.
    if is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand]) and not is_brand_carved(brane_state, brand_dicts[chosen_brand]):
        print("Obvious choice!!")
        choices.clear()
        if down_tile_land_value == 0 or down_tile_land_value == 1:
            choices.add("D")
        if left_tile_land_value == 0 or left_tile_land_value == 1:
            choices.add("L")
        if up_tile_land_value == 0 or up_tile_land_value == 1:
            choices.add("U")
        if right_tile_land_value == 0 or right_tile_land_value == 1:
            choices.add("R")
    
    stupid_horse = []
    for x in choices:
        stupid_horse.append(x)
    
    stupid_horse.sort()
    
    ## Finder debug ##
    if not stupid_flaggot and finder_debug:
        predestined_choice = known_solutions[chosen_brane+"+"+chosen_brand][len(working_moves)]
        
        if predestined_choice not in choices:
            print("Choices would've been: "+str(stupid_horse))
            error = input("Predestined choice was removed by choices algorith. Something needs to be changed.")
        
        print("Choices would've been: "+str(stupid_horse))
        
        return [predestined_choice]
    
    return stupid_horse

## The dictionaries! ##
brane_dicts = {
    "add": [
        1, 0, 0, 3, 0, 1,
        0, 0, 0, 1, 1, 0,
        0, 1, 1, 1, 1, 1,
        1, 1, create_tile_data(0, 0, 1, 1), 1, 1, 0,
        0, 1, 1, 0, 0, 0,
        1, 0, 0, 0, 0, 1,
    ],
    "eus": [
        2, 2, 2, 2, 2, 2,
        2, 2, create_tile_data(0, 0, 1, 1), 1, 2, 2,
        2, 2, 1, 2, 2, 2,
        2, 2, 2, 2, 2, 2,
        2, 2, 2, 0, 2, 2,
        2, 2, 2, 3, 2, 4,
    ],
    ## Beaver not yet impleme... bee. BEEver. Oh my god I just got that.
    "bee": [
        0, 0, 1, 1, 1, 0,
        0, 1, 1, 0, 1, 1,
        0, 1, 0, 0, 0, 1,
        0, 1, 0, create_tile_data(0, 0, 1, 1), 1, 0,
        1, 0, 0, 0, 1, 1,
        4, 1, 1, 1, 1, 0,
    ],
    ## Buttons are irrelevant for this SHIT WAIT NO THEY'RE NOT IF THE STAIRS ARE INACTIVE.,..,
    ## Corner rocks are treated as walls because that's what they are.
    "mon": [
        create_tile_data(2, 0, 0, 1), 1, 1, 1, 1, 4,
        1, 2, 2, 2, 2, 1,
        1, 2, 1, 2, 2, 1,
        1, 2, 2, create_tile_data(0, 0, 1, 1), 2, 1,
        1, 2, 2, 2, create_tile_data(1, 0, 0, 2), 1,
        4, 1, 1, 1, 1, 3,
    ],
    ## This is spaghetti
    "tan": [
        create_tile_data(1, 0, 0, 1), create_tile_data(4, 0, 0, 2), create_tile_data(0, 0, 1, 1), 1, create_tile_data(4, 0, 0, 2), create_tile_data(1, 0, 0, 1),
        create_tile_data(4, 0, 0, 2), create_tile_data(4, 0, 0, 2), 1, 1, create_tile_data(4, 0, 0, 2), create_tile_data(4, 0, 0, 2),
        create_tile_data(1, 0, 0, 1), create_tile_data(4, 0, 0, 2), create_tile_data(1, 0, 0, 1), create_tile_data(1, 0, 0, 1), create_tile_data(4, 0, 0, 2), create_tile_data(1, 0, 0, 1),
        1, 1, 3, create_tile_data(4, 0, 0, 2), 1, 1,
        1, create_tile_data(4, 0, 0, 2), create_tile_data(1, 0, 0, 1), 1, create_tile_data(4, 0, 0, 2), 1,
        1, 1, create_tile_data(4, 0, 0, 2), create_tile_data(4, 0, 0, 2), 1, 1,
    ],
    # gor
    # lev
    "cif": [
        4, 1, 0, 0, 0, 4,
        0, 1, 0, 1, 0, 1,
        0, 1, 0, 0, 1, 0,
        1, 0, 1, 0, 0, 0,
        1, 0, 0, create_tile_data(0,0,1,1), 0, 0,
        4, 1, 0, 0, 0, 4,
    ]
}

####

brand_dicts = {
    "add": [
        1, 0, 0, 0, 0, 1,
        0, 0, 0, 1, 1, 0,
        0, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 0,
        0, 1, 1, 0, 0, 0,
        1, 0, 0, 0, 0, 1,
    ],
    "eus": [
        1, 1, 0, 0, 1, 1,
        0, 0, 1, 1, 0, 0,
        1, 1, 0, 0, 0, 1,
        1, 1, 1, 0, 1, 1,
        1, 1, 0, 1, 1, 1,
        1, 1, 0, 0, 1, 1,
    ],
    "bee": [
        0, 0, 0, 0, 0, 1,
        0, 0, 1, 1, 0, 0,
        1, 1, 1, 0, 0, 1,
        1, 0, 0, 1, 1, 1,
        1, 1, 0, 0, 1, 1,
        1, 1, 1, 0, 0, 1,
    ],
    "mon": [
        1, 0, 0, 0, 1, 1,
        0, 1, 1, 1, 0, 1,
        1, 1, 0, 0, 1, 1,
        0, 1, 1, 1, 0, 1,
        1, 0, 0, 0, 1, 1,
        1, 1, 1, 0, 0, 0,
    ],
    "tan": [
        1, 0, 1, 1, 0, 1,
        0, 0, 1, 1, 0, 0,
        1, 0, 1, 1, 0, 1,
        1, 1, 0, 0, 1, 1,
        1, 0, 1, 1, 0, 1,
        1, 1, 0, 0, 1, 1,
    ],
    "gor": [
        0, 0, 1, 1, 0, 0,
        0, 0, 1, 1, 0, 0,
        1, 0, 0, 1, 0, 0,
        1, 1, 0, 0, 0, 1,
        1, 1, 1, 1, 0, 0,
        1, 1, 1, 1, 0, 0,
    ],
    "lev": [
        1, 0, 0, 0, 1, 1,
        0, 0, 1, 1, 1, 1,
        1, 0, 0, 1, 0, 0,
        0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 1,
        1, 1, 0, 0, 1, 1,
    ],
    "cif": [
        1, 1, 0, 0, 0, 1,
        0, 1, 0, 1, 0, 1,
        0, 1, 0, 0, 1, 0,
        1, 0, 1, 0, 0, 0,
        1, 0, 0, 1, 0, 0,
        1, 1, 0, 0, 0, 1,
    ],
    "dis": [
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
    ],
    "trailer": [
        1, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0,
        1, 1, 0, 0, 1, 1,
        0, 0, 0, 0, 0, 0,
        1, 0, 1, 1, 0, 1,
    ]
}

#######

# ONLY used for testing.
known_solutions = {
    "add+add": ["U","R","U","Z"],
    
    "eus+eus": ["L","Z","R","U","R","D","R","L","L","R","Z","R","Z","L","L","R","Z","R","D","L","Z","D","Z","D","Z","L","D","R"],
    "eus+lev": ["L","Z","U","R","R","D","L","Z","L","R","Z","D","D","U","U","D","Z","D","D","Z","U","R","U","Z","L","D","U","Z","D","Z","D","L","Z","R","Z","U","L","Z","R","U","Z","D","Z","U","L","R","Z","R","R","Z","L","L","R","Z","R","L","Z","U","D","Z","D","R","Z","L","U","Z","D","D","Z","R","U"],
}

## ## ## ## ## ##
## ## ## ## ## ##
## ## ## ## ## ##
## ## ## ## ## ##
## ## ## ## ## ##
## ## ## ## ## ##

#### We now begin the code. ####
import random

wings = False
sword = False
endless = False

debug_deaths = False
finder_debug = True

while True:
    print("\n")
    if finder_debug:
        print("CURRENTLY IN FINDER DEBUG MODE!!!")
    print("WINGS: "+str(wings)+"\n"+"SWORD: "+str(sword)+"\n"+"ENDLESS: "+str(endless))
    
    chosen_brane = input("Starting brane?\n")
    chosen_brand = input("...And the brand?\n")

    if chosen_brane not in brane_dicts or chosen_brand not in brand_dicts:
        print("Invalid inputs. Try again.")
        continue
    elif count_solids(brand_dicts[chosen_brand]) > count_solids(brane_dicts[chosen_brane]):
        print("Target brand has more tiles than the selected brane does. This will never work!")
        continue
    elif not endless and count_solids(brand_dicts[chosen_brand]) < count_true_solids(brane_dicts[chosen_brane]):
        print("Target brand has less tiles than the selected brane does, we do not have the endless void rod, and there are not enough glass tiles to compensate. This will never work!")
        continue
    elif chosen_brand == "dis" and not brane_has_glass_question(brane_dicts[chosen_brane]):
        print("Attempting to carve the DIS brand, but the selected brane has no glass, meaning the best we could ever do is 1 lone tile. This will never work!")
        continue
    
    flag = False
    for i in range(36):
        if brane_dicts[chosen_brane][i] == 4 and brand_dicts[chosen_brand][i] == 0:
            flag = True
            break
    if flag:
        print("Target brand has an empty space where the brane has a wall. This will never work!")
        continue
    
    # Resets this as irrelevant.
    if finder_debug and not (chosen_brane+"+"+chosen_brand in known_solutions):
        print("Brane/brand combination not in solution list, disabling finder debug mode.")
        finder_debug = False
    
    working_moves = []
    previous_loops_working_moves = []
    
    bad_solutions = []
    
    finder_debug_thresholds = []
    finder_debug_chances = []
    
    solution_loop_counter = 0
    while True:
        solution_loop_counter += 1
        print("Solution loop: " + str(solution_loop_counter))
        
        if working_moves != []:
            bad_solutions.append(working_moves)
            
            if working_moves == previous_loops_working_moves:
                print("Solution finder has generated the exact same (wrong) sequence of inputs twice in a row. This nearly-certainly implies a bug.")

        previous_loops_working_moves = working_moves
        working_moves = []
        
        held_tile = []
        current_brane_layout = list(brane_dicts[chosen_brane])
        steps_since_last_glass = 0
        
        trimmings = [] # array of arrays
        
        moving_loops = 0
        last_trimmed = -1

        ## Try random moves until we get there!
        death_flag = False
        while True:
            moving_loops += 1
            if not endless and len(held_tile) > 1:
                error = input("Endless Void Rod is not enabled but length of held_tile array is > 1.")
            
            ## Did we do it?
            if is_brand_carved(current_brane_layout, brand_dicts[chosen_brand]):
                break
            
            print("Current moves: " + str(working_moves) + " while holding " + str(held_tile))
            print(display_brane(current_brane_layout))
            print(count_solids(current_brane_layout))
            
            ## Special failure states
            # Glass can't be broken...
            if count_solids(current_brane_layout)+held_valids() == count_solids(brand_dicts[chosen_brand]):
                # The brand isn't carved...
                if not is_brand_carved(current_brane_layout,brand_dicts[chosen_brane]):
                    # No wings...
                    if not wings:
                        # Not holding a solid tile...
                        if not (1 in held_tile) and not (not stairs_exitable_question() and (2 in held_tile)):
                            # There exists no 3-line for the player to traverse with.
                            if not three_line_present_strict(current_brane_layout):
                                print("Unrecoverable situation: no 3 line and glass can't be broken.")
                                death_flag = True
                                break
            
            ## YOUR TAKING TOO LONG
            if not here_be_monsters_question(brane_dicts[chosen_brane]):
                print("Trimming down repetitive movements...")
                
                # Pickup, turn 180 degrees, and place right where it was before.
                if steps_since_last_glass > 5 and len(working_moves) >= 5 and working_moves[-5] == working_moves[-2] and working_moves[-4] == "Z" and working_moves[-3] == opposite_direction_letter(working_moves[-2]) and working_moves[-1] == "Z":
                    if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == [working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]]:
                        print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                        death_flag = True
                        break
                    if finder_debug:
                        error = input("Trimming occured in predestined choices.")
                    
                    last_trimmed = moving_loops
                    trimmings.append([working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]])
                    
                    working_moves.pop()
                    working_moves.pop()
                    working_moves.pop()
                    working_moves.pop()
                # Start facing a direction, go opposite, then go right back to facing the same way.
                if steps_since_last_glass > 3 and len(working_moves) >= 3 and working_moves[-1] == working_moves[-3] and working_moves[-2] == opposite_direction_letter(working_moves[-1]):
                    if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == [working_moves[-2],working_moves[-1]]:
                        print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                        death_flag = True
                        break
                    if finder_debug:
                        error = input("Trimming occured in predestined choices.")
                    
                    last_trimmed = moving_loops
                    trimmings.append([working_moves[-2],working_moves[-1]])
                    
                    working_moves.pop()
                    working_moves.pop()
                # spin in a dizziful bliss
                elif steps_since_last_glass > 5 and len(working_moves) >= 5:
                    store = [working_moves[-5],working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]]
                    loops = [
                        # guys stop spinning clockwise
                        ["R","D","L","U","R"],
                        ["D","L","U","R","D"],
                        ["L","U","R","D","L"],
                        ["U","R","D","L","U"],
                        
                        # COUNTERCLOCKWISE!!!
                        ["R","U","L","D","R"],
                        ["U","L","D","R","U"],
                        ["L","D","R","U","L"],
                        ["D","R","U","L","D"],
                    ]
                    
                    if store in loops:
                        if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == [working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]]:
                            print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                            death_flag = True
                            break
                        if finder_debug:
                            error = input("Trimming occured in predestined choices.")
                            
                        last_trimmed = moving_loops
                        trimmings.append([working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]])
                        
                        working_moves.pop()
                        working_moves.pop()
                        working_moves.pop()
                        working_moves.pop()
            
            too_long = False
            if chosen_brane+"+"+chosen_brand in known_solutions and len(working_moves) > 2*len(known_solutions[chosen_brane+"+"+chosen_brand]):
                print("Working moves too long. Resetting...")
                death_flag = True
                too_long = True
                break
            elif len(working_moves) > 250:
                print("Working moves too long. Resetting...")
                death_flag = True
                too_long = True
                break
            elif count_solids(brand_dicts[chosen_brand]) > count_solids(current_brane_layout)+held_valids():
                print("Target brand has more tiles than the current brane state. This will never work!")
                death_flag = True
                break

            # Every so often, perform a sanity check to make sure something hasn't gone totally wrong.
            if (not brane_has_glass_question(brane_dicts[chosen_brane]) and len(working_moves) % 1 == 0):
                default_solids = count_solids(brane_dicts[chosen_brane])
                current_solids = count_solids(current_brane_layout)

                if default_solids != current_solids + held_valids():
                    print("Sanity check fucking failed!!")
                    print("Default brane state: ", default_solids)
                    print(display_brane(brane_dicts[chosen_brane]))
                    print("Current state: ",current_solids + held_valids())
                    print(display_brane(current_brane_layout))
                    error = input("")

            ## Update glass counter.
            player_index = get_player_index(current_brane_layout)
            player_land_data = get_land_value_from_tile(current_brane_layout[player_index])
            
            if (player_land_data == 2):
                steps_since_last_glass = 0
            else:
                steps_since_last_glass += 1

            ## Check for safe choices.
            safe_choices = safe_choice_list(current_brane_layout)

            ## No safe choices!
            if len(safe_choices) == 0:
                print("No safe choices... resetting...")
                death_flag = True
                break
            else:
                print("Choices are: ",safe_choices)
            
            current_move = ""
            ## Via weighted randomness, chose a move.
            while current_move == "":
                for choice in safe_choices:
                    threshold = threshold_from_choice(current_brane_layout,choice)
                    
                    # Special case to discourage looping
                    #if moving_loops - last_trimmed < 5 and len(trimmings) > 0 and trimmings[-1][-1] == choice:
                    #    threshold = 0
                    
                    if random.random() > threshold:
                        # Calculate chance of this specific choice being made out of all the others.
                        if finder_debug:
                            # Modified the safe_choices to use a sorted list instead of a set so we can know the order they come in, making the math more feasible to make accurate.
                            # Add the odds of it happening first loop plus the odds of it happening second loop etc. etc. until gains are negligible.
                            
                            non_predestined = safe_choice_list(current_brane_layout,True)
                            iteration_of_predestination = non_predestined.index(choice)
                            
                            def odds_iteration_machine(iterations):
                                sub_odds = 1
                                searching = non_predestined*iterations
                                
                                for i in range(len(non_predestined)*iterations):
                                    # The exact searched. Multiply by odds of happening.
                                    if i == iteration_of_predestination + len(non_predestined)*iterations:
                                        sub_odds *= 1-threshold_from_choice(current_brane_layout,non_predestined[i % len(non_predestined)])
                                        break
                                    # Otherwise, multiply by odd of not happening. (Random needs to be >= threshold to return True, meaning threshold is the odds of it not happening.)
                                    else:
                                        sub_odds *= threshold_from_choice(current_brane_layout,non_predestined[i % len(non_predestined)])
                            
                                if sub_odds < 0:
                                    error = input("Sub odds is negative. "+str(sub_odds))
                            
                                return sub_odds
                            
                            # Add iterations until change is negligible.
                            odds_iterations = 1
                            odds = 0
                            while True:
                                store = odds
                                odds += odds_iteration_machine(odds_iterations)
                                
                                if abs(odds - store) < 0.00000001:
                                    break
                                
                                odds_iterations += 1
                            
                            # Safety detector.
                            if len(non_predestined) == 1 and odds < 0.98:
                                error = input("Only one choice, but odds is reporting less than 100% chance. Something is wrong. "+str(odds))
                            
                            finder_debug_thresholds.append(round(threshold,3))
                            finder_debug_chances.append(round(odds,6))
                        
                        current_move = choice
                        break
            
            ## Apply the move to the list.
            working_moves += current_move

            ## Update the brane state.
            if current_move == "Z":
                full_faced_tile_data = tile_in_direction_of_player(current_brane_layout)
                faced_land_data = get_land_value_from_tile(full_faced_tile_data)
                
                # Is tile invalid for both pickup and placedown?
                if full_faced_tile_data != faced_land_data:
                    if safe_choices == {"Z"}:
                        print("Only valid move is Z but Z does nothing. Resetting...")
                        death_flag = True
                        break
                    
                    working_moves.pop()
                # Tile is valid for pickup.
                elif faced_land_data != 0 and faced_land_data != 4 and void_rod_can_take():
                    # Put tile on void rod.
                    held_tile.append(faced_land_data)

                    # Remove the tile from the world.
                    current_brane_layout[index_tile_in_direction_of_player(current_brane_layout)] = 0
                # Placing tile.
                elif full_faced_tile_data == 0 and len(held_tile) > 0:
                    # Place the tile into the world.
                    current_brane_layout[index_tile_in_direction_of_player(current_brane_layout)] = held_tile[-1]

                    # Remove the tile from the void rod.
                    held_tile.pop()
                # Cannot do anything.
                else:
                    if safe_choices == {"Z"}:
                        print("Only valid move is Z but Z does nothing. Resetting...")
                        death_flag = True
                        break
                    
                    working_moves.pop()
            elif (current_move == "D" or current_move == "L" or current_move == "U" or current_move == "R"):
                moving_tile_index = index_tile_in_direction_of_player(current_brane_layout, direction_letter_to_number(current_move))

                if moving_tile_index == -1:
                    full_moving_tile_data = 4
                    moving_land_data = 4
                else:
                    full_moving_tile_data = tile_in_direction_of_player(current_brane_layout, direction_letter_to_number(current_move))
                    moving_land_data = get_land_value_from_tile(full_moving_tile_data)

                # Update glass counter.
                if (moving_land_data == 2):
                    steps_since_last_glass = 0

                # Tile we're moving into is a pit.
                if moving_land_data == 0:
                    # If the tile we're on is glass, remove it, then do a final check to see if that carves the brand. In this specific instance, that's actually a success.
                    if player_land_data == 2:
                        current_brane_layout[player_index] = create_tile_data(0, 0, 0, 0)
                    
                    if not is_brand_carved(current_brane_layout, brand_dicts[chosen_brand]):
                        print("Error! Death by pit??")
                        death_flag = True
                        break
                # Tile is a solid tile, or glass.
                elif moving_land_data == 1 or moving_land_data == 2 or (moving_land_data == 3 and not stairs_exitable_question(current_brane_layout)):
                    # Set tiles
                    if player_land_data == 2:
                        current_brane_layout[player_index] = create_tile_data(0, 0, 0, 0)
                    else:
                        current_brane_layout[player_index] = create_tile_data(0, 0, 0, player_land_data)
                    current_brane_layout[moving_tile_index] = create_tile_data(0, 0, direction_letter_to_number(current_move), moving_land_data)
                # Tile we're moving into is active stairs.
                elif moving_land_data == 3 and stairs_exitable_question(current_brane_layout):
                    print("Error! Death by stairs??")
                    death_flag = True
                    break
                # Tile is a wall. This is basically the same as solid tile except we only change the facing direction.
                elif moving_land_data == 4:
                    current_brane_layout[player_index] = create_tile_data(0, 0, direction_letter_to_number(current_move), player_land_data)
                else:
                    error = input("Error! Cannot resolve world state! " + current_move)
            else:
                error = input("Error! Cannot resolve world state! " + current_move)

            ## Did we do it?
            if is_brand_carved(current_brane_layout, brand_dicts[chosen_brand]):
                break

        # We died, restart!
        if death_flag:
            if not too_long and debug_deaths:
                error = input("Why did we die?")
            continue
        
        break

    # We succeeded! Print the result and hang.
    print(display_brane(current_brane_layout))
    print(working_moves)
    if finder_debug:
        print("Threshold (weight) for each move (higher means lower odds): "+str(finder_debug_thresholds))
        print("Approximate chances each move would've had in regular mode: "+str(finder_debug_chances))
        
        mult_chance = 1
        
        for chance in finder_debug_chances:
            mult_chance *= chance
        
        print("Multiplicative chance: "+str(mult_chance))
        
        #j = 1
        #while True:
        #    if 1-(pow(1-mult_chance,j)) >= p/100:
        #        break
        #    j += 1
        
        # wolfram: 1-((1-x)^j) = p/100 solve for j where j > 0 and 0 < p < 100
        import math
        p = 90
        j = -1
        while True:
            if p <= 0:
                break
            
            try:
                j = math.log(1-(p/100))/math.log(1-x)
                break
            except:
                p -= 1
        
        if p == 0:
            print("Oh my godddd like, the chance of succeeding is so small the floating point math rounds it down to zero lolz. So embarrassing.")
        else:
            print("It would take "+str(j)+" iterations for there to be a >"+str(p)+"% chance of finding the solution.")
            print("If each solution-length attempt took 0.1 second, this would in priniple take "+str((j*0.1)/60)+" minutes to find.")
    blargh = input("Success! Found this route for " + chosen_brane + " brane carving " + chosen_brand)
