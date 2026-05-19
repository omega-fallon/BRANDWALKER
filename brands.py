## Terrible Python code, go! ##

## TODO and SUGGESTIONS
## - "i would recommend setting bits and then bit masking for tile properties instead of polynomial coding, cause checking divisibility might be slower "
## B107 watcher statues
## mimic movement
## sword killing
## beaver movement
## statues disappear in tan's room
## code it so statues pushed into a corner ACTUALLY turn into walls, except in tan's room

## DONE
## ADD A CACHE FOR FOUND BAD SOLUTIONS

#### Functions ####

stupid_display_crap = False
try:
    print("█")
    print("Θ")
    print("•")
except:
    stupid_display_crap = True

## Prints a brand in a readable way.
def display_brane(brane: list[int]):
    if len(brane) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane)))

    string = ""
    for i in range(36):
        string_to_add = "?"
        
        if brane[i] == void_value:
            string_to_add = "_"
        elif brane[i] == white_value:
            if stupid_display_crap:
                string_to_add = "#"
            else:
                string_to_add = "█"
        elif brane[i] == glass_value:
            string_to_add = "/"
        elif brane[i] == exit_value:
            string_to_add = "S"
        elif brane[i] == wall_value:
            string_to_add = "W"
        elif brane[i] == chain_inactive_value:
            if stupid_display_crap:
                string_to_add = "0"
            else:
                string_to_add = "Θ"
        elif brane[i] == chain_active_value:
            if stupid_display_crap:
                string_to_add = "*"
            else:
                string_to_add = "•"
        elif brane[i] == button_value:
            string_to_add = "B"
        
        if get_rock_value_from_tile(brane[i]) == rock_present_value:
            string_to_add = "R"
        elif get_rock_value_from_tile(brane[i]) == hands_present_value:
            string_to_add = "H"
        
        if get_player_value_from_tile(brane[i]) == 1:
            string_to_add = "V"
        elif get_player_value_from_tile(brane[i]) == 2:
            string_to_add = "<"
        elif get_player_value_from_tile(brane[i]) == 3:
            string_to_add = "^"
        elif get_player_value_from_tile(brane[i]) == 4:
            string_to_add = ">"

        string += string_to_add
        string += " "

        if i == 5 or i == 11 or i == 17 or i == 23 or i == 29:
            string += "\n"

    return string

# Rock value: no rock, yes rock, hands (hands!)
# Beaver value: not present, down, left, up, right (charging store somewhere else?)
# Player value: not present, down, left, up, right
# Land value: hole, walkable, glass, stairs, wall

## Given input values, returns the appropriate tile value.
base_value = 8
base_value_2 = base_value*base_value
base_value_3 = base_value*base_value*base_value

bits_per_variable = 3

player_entity_type = 0b001
beaver_entity_type = 0b010
mimic_entity_type = 0b011
rock_entity_type = 0b100

rock_present_value = 0b001
hands_present_value = 0b010

void_value = 0b000
white_value = 0b001
glass_value = 0b010
chain_inactive_value = 0b011
chain_active_value = 0b100
button_value = 0b101
exit_value = 0b110
wall_value = 0b111

def create_tile_data(entity_type: int, entity_value: int, land: int):
    if entity_type > base_value-1 or entity_value > base_value-1 or land > base_value-1 or entity_type < 0 or entity_value < 0 or land < 0:
        error = input("Error! Invalid inputs in create_tile_data()! " + str(player) + " " + str(land))

    # New data structure:
    # 3rd slot - entity type (unspecified, player, beaver, mimic, rock/hand)
    # 2nd slot - entity value (not there, down, left, up, right); for rock (no rock, yes rock, button, rock on button, hands (hands!))
    # 1st slot - land tiles value (pit, solid, glass, exit, wall)
    return (entity_type << (bits_per_variable*2)) | (entity_value << bits_per_variable) | land

## Given a tile value, extracts the entity type value.
def get_entity_type_from_tile(x: int):
    return x >> bits_per_variable*2

## Given a tile value, extracts the rock value.
def get_rock_value_from_tile(x: int):
    if get_entity_type_from_tile(x) != rock_entity_type:
        return 0
        
    x -= base_value_2*rock_entity_type
    return x >> bits_per_variable

## Given a tile value, extracts the mimic value.
def get_mimic_value_from_tile(x: int):
    if get_entity_type_from_tile(x) != mimic_entity_type:
        return 0
        
    x -= base_value_2*mimic_entity_type
    return x >> bits_per_variable
## Given a tile value, extracts the beaver value.
def get_beaver_value_from_tile(x: int):
    if get_entity_type_from_tile(x) != beaver_entity_type:
        return 0
        
    x -= base_value_2*beaver_entity_type
    return x >> bits_per_variable

## Given a tile value, extracts the player value.
def get_player_value_from_tile(x: int):
    if get_entity_type_from_tile(x) != 1:
        return 0
        
    x -= base_value_2#*1
    return x >> bits_per_variable
    
## Given a tile value, extracts the land value.
def get_land_value_from_tile(x: int):
    while x >= base_value_2:
        x -= base_value_2
    while x >= base_value:
        x -= base_value
    return x

## Given a brane state and a brand, returns true if the brand is currently successfully carved.
def is_brand_carved(brane_state: list[int], brand: list[int]):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(base_value-1, base_value-1, base_value-1):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if i_brane_state_land == void_value and brand[i] == 0:
            continue
        elif i_brane_state_land != void_value and i_brane_state_land != exit_value and brand[i] == 1:
            continue
        return False

    return True
    
## Given a brane state and a brand, returns true if the brand is currently successfully carved, treating stairs as void.
def is_brand_carved_minus_stairs(brane_state: list[int], brand: list[int]):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(base_value-1, base_value-1, base_value-1):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if (i_brane_state_land == void_value or i_brane_state_land == exit_value) and brand[i] == 0:
            continue
        elif i_brane_state_land != void_value and i_brane_state_land != exit_value and brand[i] == 1:
            continue
        return False

    return True
    
## Given a brane state and a brand, returns true if the brand would be successfully carved if the tile the player is currently standing on is glass and was removed.
def is_brand_carved_minus_stood_glass(brane_state: list[int], brand: list[int]):
    ## First, validate the inputs to avoid any dumb mistakes.
    for i in range(36):
        if brane_state[i] < 0 or brane_state[i] > create_tile_data(base_value-1, base_value-1, base_value-1):
            error = input("Error! Invalid brane_state input in is_brand_carved()! " + display_brane(brane_state))

        if brand[i] != 0 and brand[i] != 1:
            error = input("Error! Invalid brand input in is_brand_carved! " + str(brand))

    ## Now, check in earnest.
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        if brand[i] == 0 and i_brane_state_land == void_value:
            continue
        elif brand[i] == 1 and i_brane_state_land != void_value and i_brane_state_land != exit_value:
            continue
        elif brand[i] == 0 and i_brane_state_land == glass_value and get_entity_type_from_tile(brane_state[i]) == player_entity_type:
            continue
        return False

    return True

## Given a brane state, returns the index of the player's position.
def get_player_index(brane_state: list[int], handling_absent_case = False):
    store = -1
    for i in range(36):
        if get_entity_type_from_tile(brane_state[i]) == player_entity_type:
            if store != -1:
                error = input("Error! Multiple players found by get_player_index()\n"+ display_brane(brane_state))

            store = i

    if store != -1 or handling_absent_case:
        return store

    error = input("Error! Player could not be found by get_player_index()!\n"+ display_brane(brane_state))

## Given a brane state, returns the index of the stairs.
def get_stairs_index(brane_state: list[int]):
    store = -1
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == exit_value:
            if store != -1:
                error = input("Error! Multiple stairs found by get_stairs_index()!\n"+ display_brane(brane_state))

            store = i

    if store != -1:
        return store

    error = input("Error! Stairs could not be found by get_stairs_index()!\n"+ display_brane(brane_state))

## Given a brane state, returns the land value of the tile the player is standing on.
def get_player_land_value(brane_state: list[int]):
    return get_land_value_from_tile(brane_state[get_player_index(brane_state)])

## Given a brane state, returns the player's facing value.
def get_player_direction(brane_state: list[int]):
    return get_player_value_from_tile(brane_state[get_player_index(brane_state)])

## Given a brane state, returns the player's facing value as a letter.
def player_faced_direction_letter(brane_state: list[int]):
    return ["D", "L", "U", "R"][get_player_direction(brane_state) - 1]

## Given a facing letter, returns the equivalent number.
def direction_letter_to_number(letter : str):
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
def index_tile_in_direction_of_player(brane_state: list[int], player_direction=-1):
    player_i = get_player_index(brane_state)
    if player_direction == -1 or player_direction == "X":
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
def tile_in_direction_of_player(brane_state: list[int], forced_direction=-1):
    i = index_tile_in_direction_of_player(brane_state, forced_direction)

    if i == -1:
        return wall_value
    else:
        return brane_state[i]

## Land value convenience functions
def get_down_tile_land_value(brane_state: list[int]):
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,"D"))
def get_left_tile_land_value(brane_state: list[int]):
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,"L"))
def get_up_tile_land_value(brane_state: list[int]):
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,"U"))
def get_right_tile_land_value(brane_state: list[int]):
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,"R"))

## Returns true if the void rod can take a file.
def void_rod_can_take():
    return len(held_tiles) == 0 or endless

## Returns the opposite direction of the input. Returns a letter if inputted a letter and a number if inputted a number.
def opposite_direction(x):
    if x == "U":
        return "D"
    elif x == "D":
        return "U"
    elif x == "L":
        return "R"
    elif x == "R":
        return "L"
    elif x == 1:
        return 3
    elif x == 2:
        return 4
    elif x == 3:
        return 1
    elif x == 4:
        return 2
    else:
        return "X"

## Returns true if there any MOVING monsters in the brane. Because this is used to determine if turn-wasting is worthwhile, hands (hands!) are not counted.
def here_be_monsters_question(brane_state: list[int]):
    for i in range(36):
        if get_entity_type_from_tile(brane_state[i]) == beaver_entity_type or get_entity_type_from_tile(brane_state[i]) == mimic_entity_type:
            return True

    return False

## Returns true if the input brane state has any breakable tiles in it.
breakables = [glass_value, chain_inactive_value, chain_active_value]
def brane_has_breakable_question(brane_state: list[int]):
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) in breakables:
            return True
    return False

## Returns true if the input brane state has an exit.
def brane_has_stairs_question(brane_state: list[int]):
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == exit_value:
            return True
    return False

## Counts brand-valid tiles.
def count_valids(brane_state: list[int]):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    counter = 0
    for i in range(36):
        if (get_land_value_from_tile(brane_state[i]) != void_value and get_land_value_from_tile(brane_state[i]) != exit_value):
            counter += 1
    return counter

## Counts state-1 tiles.
def count_state_1s(brane_state: list[int]):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    counter = 0
    for i in range(36):
        if (get_land_value_from_tile(brane_state[i]) == white_value):
            counter += 1
    return counter

## Checks if the stairs are active (i.e., available to exit from)
def stairs_exitable_question(brane_state: list[int]):
    if len(brane_state) != 36:
        error = input("Error! Brane with invalid length: " + str(len(brane_state)))

    # Check the rod first.
    if exit_value in held_tiles:
        return False

    # Check the brane.
    for i in range(36):
        if get_land_value_from_tile(brane_state[i]) == button_value:
            # Button doesn't have a rock on it but does have a non-player entity on it.
            if get_entity_type_from_tile(brane_state[i]) == beaver_entity_type or get_entity_type_from_tile(brane_state[i]) == mimic_entity_type:
                pass
            else:
                return False

    return True

## Returns the number of valid tiles currently held by the wand.
def held_valids():
    counter = 0
    for x in held_tiles:
        if x != 0 and x != 3:
            counter += 1
    return counter
    
## Gives a value representing the "distance" between a brane state and the solution. This is calculated as the number of mismatched tiles, NOT distance in a state-space way. What, do you think I'm competent at coding or something?
def distance_from_heaven(brane_state: list[int], brand: list[int]):
    distance = 0
    
    for i in range(36):
        i_brane_state_land = get_land_value_from_tile(brane_state[i])
        
        if i_brane_state_land == void_value and brand[i] == 0:
            continue
        elif i_brane_state_land != void_value and i_brane_state_land != exit_value and brand[i] == 1:
            continue
        
        distance += 1
        
    # Failure states get special penalty.
    if get_player_index(brane_state, handling_absent_case = True) == -1:
        distance += 10
    else:
        if special_failure_states(brane_state):
            distance += 10
        if len(safe_choice_list(brane_state,True)) == 0:
            distance += 10
    
    return distance
    
## Returns taxicab distance between two points on the brane room, given by their index.
def taxicab_distance(a: int, b: int):
    x1 = a % 6
    y1 = int(a/6)
    
    x2 = b % 6
    y2 = int(b/6)
    
    return abs(x1 - x2) + abs(y1 - y2)
    
## Returns True if player is floating.
def floating(brane_state: list[int]):
    return get_player_land_value(brane_state) == void_value
    
## Returns True if the tile is undesirable (or impossible) to move into. Takes a land value.
def land_undesirable(land: int, brane_state: list[int]):
    return ((land == void_value or land == chain_active_value) and wings and floating(brane_state)) or ((land == void_value or land == chain_active_value) and not wings) or land == wall_value or (land == exit_value and stairs_exitable_question(brane_state))
    
## Cleaner stringification for arrays of moves.
def array_stringify(array: list[str]):
    string = ""
    for x in array:
        string += x
    return string
    
## Given the state and an input, returns the predicted change in "solution distance" if the player were to take that action.
## Positive change indicates increasing distance, while negative represents lowering the distance. Thus, here, negative is desirable.
def predicted_distance_change(brane_state: list[int], input_letter: str):
    total = 0
    
    brand = brand_dicts[chosen_brand]
    
    faced_tile = tile_in_direction_of_player(brane_state)
    faced_tile_land_value = get_land_value_from_tile(faced_tile)
    
    if input_letter == "Z":
        # Player is placing a tile.
        if faced_tile_land_value == void_value and len(held_tiles) != 0:
            # Player is placing stairs.
            if held_tiles[-1] == exit_value:
                total += 1
            # Player is placing a tile where the brand has a solid tile.
            elif brand[index_tile_in_direction_of_player(brane_state)] == 1:
                total += -1
            # Player is placing a tile where the brand does NOT have a solid tile.
            else:
                total += 1
        # Player is picking up a tile.
        elif faced_tile_land_value != void_value and faced_tile_land_value != wall_value and void_rod_can_take():
            # Player is picking up stairs.
            if faced_tile_land_value == exit_value:
                total += -1
            # Player is picking up a tile where the brand has an empty tile.
            elif brand[index_tile_in_direction_of_player(brane_state)] == void_value:
                total += -1
            else:
                total += 1
    elif input_letter == "D" or input_letter == "L" or input_letter == "U" or input_letter == "R":
        # Standing on glass.
        if get_player_land_value(brane_state) == glass_value:
            # Tile we're moving into is moveinto-able, but not glass
            if not (faced_tile_land_value == exit_value and stairs_exitable_question(brane_state)) and faced_tile_land_value != wall_value:
                # Determine the effect of this action.
                if brand[get_player_index(brane_state)] == 0:
                    total += -1
                else:
                    total += 1
           
        # Moving into glass
        if faced_tile_land_value == glass_value:
            if brand[index_tile_in_direction_of_player(brane_state)] == 0:
                total += -1
            else:
                total += 1
        # Moving onto an active chain tile.
        elif faced_tile_land_value == chain_active_value and wings and not floating(brane_state):
            total += distance_from_heaven(trigger_chain_disperse(list(brane_state),index_tile_in_direction_of_player(brane_state,letter))) - distance_from_heaven(brane_state)
                    
        # Fractional weights for moving closer to the stairs.
        if brane_has_stairs_question(brane_state):
            total += (taxicab_distance(index_tile_in_direction_of_player(brane_state),get_stairs_index(brane_state)) - taxicab_distance(get_player_index(brane_state),get_stairs_index(brane_state))) / 3
            
    # What is the average distance from Heaven among all prior iterations beginning here?
    total_distance = 0
    paths_matched = 0
    
    for i in range(len(bad_solutions)):
        walked_path : str = bad_solutions[i]
        
        # Check if we'd go out of bounds.
        a : str = working_moves + input_letter
        if len(a) > len(walked_path):
            continue
        
        # See if the paths match.
        flag = False
        for i2 in range(len(a)):
            if a[i2] != walked_path[i2]:
                break
            flag = True
            
        # Match found!
        paths_matched += 1
        total_distance += bad_solutions_distance[i]
        
        # Slight tilt, increase perceived distance if the path is short. (Died.)
        total_distance += min(20,(20 - len(walked_path)))
        
    # Average and add as factor.
    if paths_matched > 0:
        scaling_factor = 6*6
        total += (total_distance/paths_matched)/scaling_factor
        
        global weirdo_flag
        weirdo_flag = True
        #print("THEYDIES AND GENTLETHEMS, WE GOT 'EM.")
        
    # Failsafe: distance is 0.
    return total
    
## Based on brane state and choice, returns the threshold based on its prediction.
def threshold_from_choice(brane_state: list[int],choice):
    # \min\left(0.95,\max\left(0.05,0.5\cdot\frac{\left(x+1.5\right)}{\left(1.5\right)}\right)\right)
    
    slant_factor = 5
    threshold = 0.5*((predicted_distance_change(brane_state,choice)+slant_factor)/slant_factor)
    
    # Clamp the threshold so that nothing is ever truly certain or impossible
    if threshold > 0.95:
        threshold = 0.95
    elif threshold < 0.05:
        threshold = 0.05
        
    return threshold
    
## Given an i value for a brane array and movements on the x and y axis, returns a new i index corresponding to that movement.
def move_cartesian(i: int, x: int, y: int):
    store = i + x + 6*y
    
    if store > 35 or store < 0 or int(i/6) != int ((i+x)/6):
        return -1
    else:
        return store
    
## Given a starting position and cartesian movements, returns the full tile value of the tile at that index. Accounts for OOB searching.
def tile_at_moved_cartesian(i: int, brane_state: list[int], x: int, y: int):
    store = move_cartesian(i, x, y)
    
    if store == -1:
        return wall_value
    else:
        return brane_state[store]
    
## Given a starting position and cartesian movements, returns the land value of the tile at that index. Accounts for OOB searching.
def land_at_moved_cartesian(i: int, brane_state: list[int], x: int, y: int):
    store = move_cartesian(i, x, y)
    
    if store == -1:
        return wall_value
    else:
        return get_land_value_from_tile(brane_state[store])
    
## Returns true if the land value of this tile is 1 or (3, inactive).
def effective_type_1(i: int, brane_state: list[int]):
    return (get_land_value_from_tile(i) == white_value or (get_land_value_from_tile(i) == exit_value and not stairs_exitable_question(brane_state))) and get_entity_type_from_tile(i) == 0
    
## Returns true if there is a 3 line of moveable land tiles. This includes only type-1 and inactive type-3.
def three_line_present_strict(brane_state: list[int]):
    for i in range(36):
        
        if i + 3 <= 35 and int(i/6) == int((i+3)/6) and effective_type_1(brane_state[i],brane_state) and effective_type_1(brane_state[i+1],brane_state) and effective_type_1(brane_state[i+2],brane_state):
            return True
        if i + 6*2 <= 35 and effective_type_1(brane_state[i],brane_state) and effective_type_1(brane_state[i+6],brane_state) and effective_type_1(brane_state[i+12],brane_state):
            return True
            
    return False
    
## Given a brane layout and starting position, triggers a chain dispersion.
def trigger_chain_disperse(brane_state: list[int], i: int):
    if i < 0:
        return brane_state
    
    triggered_tiles = {i}
    
    done_something = True
    while done_something:
        done_something = False
        
        for triggered_i in triggered_tiles:
            # Confirm land.
            if get_land_value_from_tile(brane_state[triggered_i]) != chain_active_value:
                error = input("triggered_i isn't an active chain: "+str(triggered_i)+" "+str(triggered_tiles))
                
            # Check each direction.
            if triggered_i-1 >= 0 and triggered_i-1 not in triggered_tiles and get_land_value_from_tile(brane_state[triggered_i-1]) == chain_active_value:
                done_something = True
                triggered_tiles.add(triggered_i-1)
                break
            if triggered_i+1 <= 35 and triggered_i+1 not in triggered_tiles and get_land_value_from_tile(brane_state[triggered_i+1]) == chain_active_value:
                done_something = True
                triggered_tiles.add(triggered_i+1)
                break
            if triggered_i-6 >= 0 and triggered_i-6 not in triggered_tiles and get_land_value_from_tile(brane_state[triggered_i-6]) == chain_active_value:
                done_something = True
                triggered_tiles.add(triggered_i-6)
                break
            if triggered_i+6 <= 35 and triggered_i+6 not in triggered_tiles and get_land_value_from_tile(brane_state[triggered_i+6]) == chain_active_value:
                done_something = True
                triggered_tiles.add(triggered_i+6)
                break
                
    # Remove the tiles.
    for triggered_i in triggered_tiles:
        brane_state[triggered_i] = 0
        
    return brane_state
    
## Shorthand for a use case of the above.
def trigger_chain_disperse_direction(brane_state: list[int], direction):
    return trigger_chain_disperse(brane_state,index_tile_in_direction_of_player(brane_state,direction))
    
## Given a brane layout, returns the list of not-obviously-stupid inputs.
cardinals = ["D","L","U","R"]
def safe_choice_list(brane_state: list[int], stupid_flaggot: bool = False):
    choices = {"D", "L", "U", "R", "Z"}

    down_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, "D"))
    left_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, "L"))
    up_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, "U"))
    right_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, "R"))

    faced_tile = tile_in_direction_of_player(brane_state)
    faced_tile_land_value = get_land_value_from_tile(faced_tile)

    ## Deadly or round-ending ##
    for key, value in {"D": down_tile_land_value, "L": left_tile_land_value, "U": up_tile_land_value, "R": right_tile_land_value}.items():
        # Going down stairs.
        if value == exit_value and stairs_exitable_question(brane_state):
            choices.remove(key)
        # Falling into a pit while wingless or floating without standing on glass that's the last piece to remove before the brand is carved.
        elif value == void_value:
            if not wings or floating(brane_state):
                if not is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand]):
                    choices.remove(key)
        # Stepping on an active chain while wingless or floating which wouldn't result in the brand being carved.
        elif value == chain_active_value:
            if not wings or floating(brane_state):
                if not (value == chain_active_value and is_brand_carved(trigger_chain_disperse_direction(list(brane_state), key), brand_dicts[chosen_brand])):
                    choices.remove(key)
        ## Breaking a piece of glass that brings total carve-valid tiles below the brand's amount.
        elif value == glass_value and count_valids(brane_state)+held_valids() == count_valids(brand_dicts[chosen_brand]):
            choices.remove(key)
        
    ## Dumb but not deadly ##
    ## There is no tile in front of the player and the player does not have any tile stored. There is no point in pressing "Z"
    if faced_tile_land_value == void_value and len(held_tiles) == 0:
        choices.remove("Z")
    ## There is a tile in front of the player and the player lacks the ability to take it. There is no point in pressing "Z"
    elif faced_tile_land_value != void_value and not void_rod_can_take():
        choices.remove("Z")
    ## Special case.
    elif (chosen_brand == "add" and chosen_brane == "add") or (chosen_brand == "lev" and chosen_brane == "lev"):
        if not (faced_tile_land_value == exit_value and void_rod_can_take()):
            choices.remove("Z")

    ## The tile in front is a wall, and there are no monsters to make wasting a turn meaningful.
    ## Hitting a wall to your side CAN be useful to reposition, so we will not discount it!
    if faced_tile_land_value == wall_value and not here_be_monsters_question(brane_state) and player_faced_direction_letter(brane_state) in choices:
        choices.remove(player_faced_direction_letter(brane_state))

    ## Pointless movements (repetitive ones are trimmed afterward, not outright removed) ##
    if not here_be_monsters_question(brane_state):
        # Entering a dead end. (Dumb bun.)
        if get_player_land_value(brane_state) not in breakables:
            player_index = get_player_index(brane_state)
            
            for x in cardinals:
                # Don't check to see if the land is moveable; if it hasn't been removed by an earlier filter, it is.
                if x not in choices:
                    continue
                
                #print("wonderwall\n"+display_brane(brane_state))
                # Confirm potential movement tile attributes and make pawn tile variables.
                if x == "D" and down_tile_land_value not in breakables and not land_undesirable(down_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,2)
                elif x == "L" and left_tile_land_value not in breakables and not land_undesirable(left_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,-2,0)
                elif x == "U" and up_tile_land_value not in breakables and not land_undesirable(up_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,-2)
                elif x == "R" and right_tile_land_value not in breakables and not land_undesirable(right_tile_land_value,brane_state):
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,2,0)
                else:
                    continue
                
                pawn_land_value_backwards = get_land_value_from_tile(tile_in_direction_of_player(brane_state,opposite_direction(x)))
                
                # Ignore if at the end of the "dead end" we could potentially place or pick up a tile. That makes it useful.
                if (pawn_land_value_first_turn == void_value and len(held_tiles) > 0) or (pawn_land_value_first_turn != void_value and pawn_land_value_first_turn != wall_value and void_rod_can_take()):
                    pass
                # Ignore if the tile behind the player is empty and the void rod can place, or solid and the void rod can take. This could be a useful repositioning tactic.
                elif (pawn_land_value_backwards == void_value and len(held_tiles) > 0) or (void_rod_can_take() and pawn_land_value_backwards != void_value and pawn_land_value_backwards != wall_value):
                    pass
                # Remove if dead end.
                elif land_undesirable(pawn_land_value_attack_1, brane_state) and land_undesirable(pawn_land_value_attack_2, brane_state) and land_undesirable(pawn_land_value_first_turn, brane_state):
                    print("Pawn values found to be dead end:",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    print("Direction:",x)
                    choices.remove(x)
                else:
                    pass
                    #print("Pawn values found not to be dead end:",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    #print("Direction:",x)
    
    #print("because you're so smooth")
    if not here_be_monsters_question(brane_state) and "Z" in choices:
        # Double z's are never useful without monsters
        if len(working_moves) > 0 and working_moves[-1] == "Z":
            choices.remove("Z")
        # Trapping yourself is never worth it. (The "final stairs" case is overridden in a later block, disregard.)
        elif not wings and void_rod_can_take() and faced_tile_land_value != 0 and brane_has_stairs_question(brane_state) and int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state)) == 3:
            choices.remove("Z")
    
    #print("one week")
    ## Historically bad choices ##
    for choice in {"D","L","U","R","Z"}:
        if (working_moves + choice) in bad_solutions and choice in choices:
            choices.remove(choice)
            #notice = input("We learned a lesson!! "+str(working_moves + choice)+" against "+str(choice))
            
    #print("somebody once told me")
    ## Obviously correct choices ##
    if not is_brand_carved(brane_state, brand_dicts[chosen_brand]):
        # If removing the stairs is the last step and we're already facing them, always do that.
        if is_brand_carved_minus_stairs(brane_state, brand_dicts[chosen_brand]) and faced_tile_land_value == exit_value and void_rod_can_take():
            choices = {"Z"}
        # If breaking the glass we're currently on is the last step, always do that.
        elif is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand]):
            print("Obvious choice!!")
            choices.clear()
            if down_tile_land_value == void_value or down_tile_land_value == white_value or (down_tile_land_value == exit_value and not stairs_exitable_question(brane_state)):
                choices.add("D")
            if left_tile_land_value == void_value or left_tile_land_value == white_value or (left_tile_land_value == exit_value and not stairs_exitable_question(brane_state)):
                choices.add("L")
            if up_tile_land_value == void_value or up_tile_land_value == white_value or (up_tile_land_value == exit_value and not stairs_exitable_question(brane_state)):
                choices.add("U")
            if right_tile_land_value == void_value or right_tile_land_value == white_value or (right_tile_land_value == exit_value and not stairs_exitable_question(brane_state)):
                choices.add("R")
        # Dispersing chain tiles to carve the brand.
        else:
            if down_tile_land_value == chain_active_value and is_brand_carved(trigger_chain_disperse_direction(list(brane_state), "D"), brand_dicts[chosen_brand]):
                choices.add("D")
            if left_tile_land_value == chain_active_value and is_brand_carved(trigger_chain_disperse_direction(list(brane_state), "L"), brand_dicts[chosen_brand]):
                choices.add("L")
            if up_tile_land_value == chain_active_value and is_brand_carved(trigger_chain_disperse_direction(list(brane_state), "U"), brand_dicts[chosen_brand]):
                choices.add("U")
            if right_tile_land_value == chain_active_value and is_brand_carved(trigger_chain_disperse_direction(list(brane_state), "R"), brand_dicts[chosen_brand]):
                choices.add("R")
    
    stupid_horse = []
    for x in choices:
        stupid_horse.append(x)
    
    stupid_horse.sort()
    
    ## PREDESTINATION MODE ##
    if not stupid_flaggot and predestination_mode:
        predestined_choice = known_solutions[combo_name()][len(working_moves)]
        
        if predestined_choice not in choices:
            print("Choices would've been: "+str(stupid_horse))
            error = input("Predestined choice was removed by choices algorithm. Something needs to be changed.")
        
        print("Choices would've been: "+str(stupid_horse))
        
        return [predestined_choice]
    
    return stupid_horse

## Given a brane state, converts to a hashable (dictionary key–valid) form
def hashable_brane_state(brane_state: list[int]):
    string = ""
    for i in range(36):
        string += bin(brane_state[i])
    return string

## Given a brand layout, checks to see if there's anything that can definitively prove which brand room we're in. If it can, it returns that Void Lord's name, otherwise it returns an empty string.
def prove_void_lord(brane_state: list[int]):
    # fill in
    
    return ""

## Generates a random brane state. By default, it excludes only truly impossible things like multiple players and exits, but (in the future) it can be toggled to be made more restrictive.
def random_brane():
    # Choices to choose from
    valid_lands = [void_value, white_value, glass_value, chain_inactive_value, chain_active_value, button_value, exit_value]#, wall_value]
    valid_entities = [0,player_entity_type, beaver_entity_type, mimic_entity_type, rock_entity_type]
        
    # These will help eliminate configurations irrelevant to our purpose.
    add_whites = 18
    eus_whites = 3
    bee_whites = 18
    mon_whites = 18
    tan_whites = 22
    gor_whites = 11
    lev_whites = 14
    cif_whites = 11
    
    add_glass = 0
    eus_glass = 30
    bee_glass = 0
    mon_glass = 14
    tan_glass = 13#?
    gor_glass = 23
    lev_glass = 0
    cif_glass = 0
    
    add_walls = []
    eus_walls = [35]
    bee_walls = [30]
    mon_walls = [5,30]
    tan_walls = []# Tan's room is considered to have no walls due to disappearing statues
    gor_walls = [30]
    lev_walls = [0,30]
    cif_walls = [0,5,30,35]
    martin_walls = "what"
    
    max_whites = max(add_whites,eus_whites,bee_whites,mon_whites,tan_whites,gor_whites,lev_whites,cif_whites)
    placed_whites = 0
    
    max_glass = 30
    placed_glass = 0
    
    max_chains = 19
    placed_chains = 0
    
    max_rocks = 7
    placed_rocks = 0
    
    max_hands_hands = 13
    placed_hands_hands = 0
    
    placed_buttons = 0
    
    room_monster = "" # Beavers, mimics, and hands are mutually exclusive.
    
    array = []
    
    for i in range(36):
        # Land
        # Attempt to place a wall
        if i == 0 or i == 5 or i == 30 or i == 35:
            # Is a wall valid here? See if we can definitively determine what room we're in and check that way.
            
            # Eus
            if placed_glass >= eus_glass and (i == 0 or i == 5 or i == 30):
                land = random.choice(valid_lands)
                
            # Bee
            elif room_monster == "beaver" and (i == 0 or i == 5 or i == 35):
                land = random.choice(valid_lands)
                
            # Mon can get a wall added by the rock that exists in the room.
            
            # Tan
            elif room_monster == "hands!":
                land = random.choice(valid_lands)
                
            # Gor and Lev can get a wall added by the rock that exists in the room.
            
            # Miscellaneous. top right & bottom right without bottom left is impossible.
            elif i == 35 and array[30] != wall_value and array[5] == wall_value:
                land = random.choice(valid_lands)
                
            else:
                land = random.choice(valid_lands + [wall_value])
                
                # Eliminations
                if land == wall_value:
                    # Bee
                    if beaver_entity_type in valid_entities and (i == 0 or i == 5 or i == 35):
                        valid_entities.remove(beaver_entity_type)
                        
        else:
            land = random.choice(valid_lands)
            
        if land == white_value:
            # Maximum on whites
            placed_whites += 1
            if placed_whites == max_whites:
                valid_lands.remove(white_value)
            elif placed_whites > max_whites:
                error = input("Random brane: max whites exceeded: "+str(placed_whites)+"/"+str(max_whites))
                valid_lands.remove(white_value)
                
            # The maximum of all brand rooms with glass
            if placed_whites >= max(eus_whites,mon_whites,gor_whites):
                # We've already placed glass.
                if placed_glass > 0:
                    # We're exactly at the limit.
                    if placed_whites == max(eus_whites,mon_whites,gor_whites) and white_value in valid_lands:
                        valid_lands.remove(white_value)
                    # Above the limit.
                    else:
                        error = input("Random brane: brane has glass, but more white tiles placed than is valid for branes with glass.")
                # No glass has been placed.
                elif glass_value in valid_lands:
                    valid_lands.remove(glass_value)
            # Excess whites means we can't be in Bee's room
            if placed_whites > bee_whites:
                if room_monster == "beaver":
                    error = input("Random brane: beaver present but more whites than Bee's room.")
                elif beaver_entity_type in valid_entities:
                    valid_entities.remove(beaver_entity_type)
            # Excess whites means we can't be in Mon's room
            if placed_whites > mon_whites:
                if placed_buttons > 0:
                    error = input("Random brane: have a button (in Mon's room) have more whites than his room has.")
                elif button_value in valid_lands:
                    valid_lands.remove(button_value)
            # Excess whites means we can't be in Gor's room
            if placed_whites > gor_whites:
                if room_monster == "mimic":
                    error = input("Random brane: mimic present but more whites than Gor's room.")
                elif mimic_entity_type in valid_entities:
                    valid_entities.remove(mimic_entity_type)
            # Excess whites means we can't be in Lev's room
            if placed_whites >= lev_whites:
                if placed_chains > 0:
                    if placed_whites > lev_whites:
                        error = input("Error, chains are placed but there are more white tiles than Lev's room.")
                    valid_lands.remove(white_value)
                else:
                    if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                        error = input("Random brane: chain lands aren't both eliminated or both present")
                    elif chain_inactive_value in valid_lands:
                        valid_lands.remove(chain_inactive_value)
                        valid_lands.remove(chain_active_value)
        elif land == glass_value:
            # Maximum on glass
            placed_glass += 1
            if placed_glass == max_glass:
                valid_lands.remove(glass_value)
            elif placed_glass > max_glass:
                error = input("Random brane: max glass exceeded: "+str(placed_glass)+"/"+str(max_glass))
                valid_lands.remove(glass_value)
                
            # Stupid shit.
            if placed_whites == max(eus_whites,mon_whites,gor_whites):
                valid_lands.remove(glass_value)
            elif placed_whites >= max(eus_whites,mon_whites,gor_whites):
                error = input("Random brane: brane has glass, but more white tiles placed than is valid for branes with glass.")
            
            # Glass is incompatible with chains.
            if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                error = input("Random brane: chain lands aren't both eliminated or both present")
            elif chain_inactive_value in valid_lands:
                valid_lands.remove(chain_inactive_value)
                valid_lands.remove(chain_active_value)
            
            # Glass is incompatible with beaver.
            if beaver_entity_type in valid_entities:
                valid_entities.remove(beaver_entity_type)
            
            # Excess glass means we can't be in Bee's room
            if placed_glass > bee_glass:
                if room_monster == "beaver":
                    error = input("Random brane: beaver present but more glass than Bee's room.")
                elif beaver_entity_type in valid_entities:
                    valid_entities.remove(beaver_entity_type)
            # Excess glass means we can't be in Mon's room
            if placed_glass > mon_glass:
                if placed_buttons > 0:
                    error = input("Random brane: have a button (in Mon's room) have more glass than his room has..")
                
                if button_value in valid_lands:
                    valid_lands.remove(button_value)
            # Excess whites means we can't be in Gor's room
            if placed_glass > gor_glass:
                if room_monster == "mimic":
                    error = input("Random brane: mimic present but more glass than Gor's room.")
                elif mimic_entity_type in valid_entities:
                    valid_entities.remove(mimic_entity_type)
        elif land == chain_inactive_value or land == chain_active_value:
            # Maximum on chains
            placed_chains += 1
            if placed_chains == max_chains:
                valid_lands.remove(chain_inactive_value)
                valid_lands.remove(chain_active_value)
            elif placed_chains > max_chains:
                error = input("Random brane: max chains exceeded.")
                valid_lands.remove(chain_inactive_value)
                valid_lands.remove(chain_active_value)
                
            # Chains are incompatible with these.
            if glass_value in valid_lands:
                valid_lands.remove(glass_value)
            
            if beaver_entity_type in valid_entities:
                valid_entities.remove(beaver_entity_type)
            if mimic_entity_type in valid_entities:
                valid_entities.remove(mimic_entity_type)
            
            # Presence of chains means no monsters
            if room_monster != "" and room_monster != "peaceful":
                error = input("Random brane: trying to set peaceful but monsters already exist: "+room_monster)
            else:
                room_monster = "peaceful"
        elif land == button_value:
            # Only one button is allowed, and it's incompatible with these.
            placed_buttons += 1
            valid_lands.remove(button_value)
            
            if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                error = input("Random brane: chain lands aren't both eliminated or both present")
            elif chain_inactive_value in valid_lands:
                valid_lands.remove(chain_inactive_value)
                valid_lands.remove(chain_active_value)
            
            if beaver_entity_type in valid_entities:
                valid_entities.remove(beaver_entity_type)
            if mimic_entity_type in valid_entities:
                valid_entities.remove(mimic_entity_type)
            
            # Presence of button means no monsters
            room_monster = "peaceful"
            
            # Presence of button sets maximums on whites and glasses
            if max_whites > mon_whites:
                max_whites = mon_whites
            if max_glass > mon_glass:
                max_glass = mon_glass
        elif land == exit_value:
            valid_lands.remove(exit_value)
        
        # Entity type
        entity_type = 0
        if land != void_value and land != wall_value and land != chain_inactive_value: # Not a typo: an entity being on an inactive tile is impossible.
            entity_type = random.choice(valid_entities)
            
            # Rock can't go here!
            while room_monster != "hands!" and (i == 0 or i == 5 or i == 30 or i == 35) and entity_type == rock_entity_type:
                entity_type = random.choice(valid_entities)
            
            # Only one player allowed.
            if entity_type == player_entity_type:
                valid_entities.remove(player_entity_type)
            # Only one beaver allowed.
            elif entity_type == beaver_entity_type:
                if room_monster != "":
                    error = input("Random brane error: attempted to place mimic on brane with the following room_monster: "+room_monster)
                    
                room_monster = "beaver"
                valid_entities.remove(beaver_entity_type)
                
                # Beaver and mimic are incompatible.
                if mimic_entity_type in valid_entities:
                    valid_entities.remove(mimic_entity_type)
                
                # Glass is incompatible with beaver.
                if placed_glass > 0:
                    error = input("Random brane error: attempted to place beaver on brane with glass.")
                else:
                    valid_lands.remove(glass_value)
                    
                # Chains are incompatible with beaver.
                if placed_chains > 0:
                    error = input("Random brane error: attempted to place beaver on brane with chains.")
                else:
                    if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                        error = input("Random brane: chain lands aren't both eliminated or both present")
                    elif chain_inactive_value in valid_lands:
                        valid_lands.remove(chain_inactive_value)
                        valid_lands.remove(chain_active_value)

                # Buttons are incompatible with beaver.
                if button_value in valid_lands:
                    valid_lands.remove(button_value)
                  
                # Presence of beaver sets maximum on white
                if max_whites > bee_whites:
                    max_whites = bee_whites
            # Only one mimic allowed.
            elif entity_type == mimic_entity_type:
                if room_monster != "":
                    error = input("Random brane error: attempted to place mimic on brane with the following room_monster: "+room_monster)
                
                room_monster = "mimic"
                valid_entities.remove(mimic_entity_type)
                
                # Beaver and mimic are incompatible.
                if beaver_entity_type in valid_entities:
                    valid_entities.remove(beaver_entity_type)
                
                # Chains are incompatible with mimics.
                if placed_chains > 0:
                    error = input("Random brane error: attempted to place beaver on brane with chains.")
                else:
                    if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                        error = input("Random brane: chain lands aren't both eliminated or both present")
                    elif chain_inactive_value in valid_lands:
                        valid_lands.remove(chain_inactive_value)
                        valid_lands.remove(chain_active_value)
                        
                # Presence of mimic sets maximums on whites and glasses.
                if max_whites > gor_whites:
                    max_whites = gor_whites
                if max_glass > gor_glass:
                    max_glass = gor_glass
            elif entity_type == rock_entity_type:
                placed_rocks += 1
                
                # Maximum on rocks.
                if placed_rocks - placed_hands_hands == max_rocks:
                    valid_entities.remove(rock_entity_type)
                elif placed_rocks - placed_hands_hands > max_rocks:
                    error = input("Random brane: max rocks exceeded.")
                    valid_entities.remove(rock_entity_type)
                
                # B179 has only one rock.
                if placed_chains > 0:
                    max_rocks = 1
                    valid_entities.remove(rock_entity_type)
                
        # Include chance for floating player.
        elif land == void_value and wings and player_entity_type in valid_entities:
            entity_type = random.choice([0,player_entity_type])
            if entity_type == player_entity_type:
                valid_entities.remove(player_entity_type)
        
        # Then entity value
        entity_value = 0
        if entity_type == 0:
            pass
        # Rocky!
        elif entity_type == rock_entity_type:
            # Coding hands (hands!) like this is really biting me in the butt (ass)
            if (room_monster == "" or room_monster == "hands!") and not placed_hands_hands >= max_hands_hands and not (wall_value in array) and not land == exit_value and not land == button_value and not land == glass_value:
                entity_value = random.choice([rock_present_value, hands_present_value])
                room_monster = "hands!"
                
                # Add hands (hands!)
                placed_hands_hands += 1
                
                # Hands (hands!) are incompatible with these.
                if button_value in valid_lands:
                    valid_lands.remove(button_value)
                
                if beaver_entity_type in valid_entities:
                    valid_entities.remove(beaver_entity_type)
                if mimic_entity_type in valid_entities:
                    valid_entities.remove(mimic_entity_type)
                    
                if (chain_inactive_value in valid_lands)^(chain_active_value in valid_lands):
                    error = input("Random brane: chain lands aren't both eliminated or both present")
                elif chain_inactive_value in valid_lands:
                    valid_lands.remove(chain_inactive_value)
                    valid_lands.remove(chain_active_value)
                    
                # Presence of hands (hands!) sets maximum on whites and glass.
                if max_whites > tan_whites:
                    max_whites = tan_whites
                if max_glass > tan_glass:
                    max_glass = tan_glass
            else:
                entity_value = rock_present_value
        else:
            entity_value = random.choice([1,2,3,4])
        
        # Finally push
        array.append(create_tile_data(entity_type,entity_value,land))

    return array

#### State traversal function has a special spot right here. ####
## Returns nothing, directly modifying the input array. Account for this!!
def brane_walk(brane_state: list[int], input: str, state_space = False):
    global death_flag, working_moves, steps_since_last_glass, steps_since_last_bump, steps_since_last_chain
    
    if input == "Z":
        full_faced_tile_data = tile_in_direction_of_player(brane_state)
        faced_land_data = get_land_value_from_tile(full_faced_tile_data)
        
        # Slaaaaaayy the beaaast!!!
        if sword and ((get_entity_type_from_tile(full_faced_tile_data) in [beaver_entity_type, mimic_entity_type]) or get_rock_value_from_tile(full_faced_tile_data) == hands_present_value):
            brane_state[index_tile_in_direction_of_player(brane_state)] = create_tile_data(0,0,faced_land_data)
        # Is tile invalid for both pickup and placedown?
        elif full_faced_tile_data != faced_land_data or faced_land_data == wall_value: # (Explanation: this inequality means there is an entity on the tile, meaning an enemy or a rock. The second one is just checking if the tile is a wall, which is self-explanatory.) 
            if safe_choices == ["Z"]:
                print("Only valid move is Z but Z does nothing. Resetting...")
                death_flag = True
                return "death"
            
            if state_space:
                pass
            else:
                working_moves = working_moves[:-1]
        # Tile is valid for pickup.
        elif faced_land_data != void_value and faced_land_data != wall_value and void_rod_can_take():
            steps_since_last_bump += 1
            
            # Put tile on void rod.
            held_tiles.append(faced_land_data)

            # Remove the tile from the world.
            brane_state[index_tile_in_direction_of_player(brane_state)] = 0
        # Placing tile.
        elif full_faced_tile_data == void_value and len(held_tiles) > 0:
            steps_since_last_bump += 1
            
            # Place the tile into the world.
            brane_state[index_tile_in_direction_of_player(brane_state)] = held_tiles[-1]

            # Remove the tile from the void rod.
            held_tiles.pop()
        # Cannot do anything.
        else:
            if safe_choices == ["Z"]:
                print("Only valid move is Z but Z does nothing. Resetting...")
                death_flag = True
                return "death"
            
            working_moves = working_moves[:-1]
    elif (input == "D" or input == "L" or input == "U" or input == "R"):
        moving_tile_index = index_tile_in_direction_of_player(brane_state, direction_letter_to_number(input))

        if moving_tile_index == -1:
            full_moving_tile_data = wall_value
            moving_land_data = wall_value
        else:
            full_moving_tile_data = tile_in_direction_of_player(brane_state, direction_letter_to_number(input))
            moving_land_data = get_land_value_from_tile(full_moving_tile_data)

        # Moving into a hand (hands!)
        if get_rock_value_from_tile(full_moving_tile_data) == hands_present_value:
            print("Error! Death by hand?? Hands?!!")
            death_flag = True
            return
        # Moving into a rock.
        elif get_rock_value_from_tile(full_moving_tile_data) == rock_present_value:
            steps_since_last_bump = 0
            
            # Determine tile the rock is moving into.
            rock_destination_index = -1
            rock_destination_tile_value = 0
            if input == "D":
                rock_destination_index = move_cartesian(player_index,0,2)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,brane_state,0,2)
            elif input == "L":
                rock_destination_index = move_cartesian(player_index,-2,0)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,brane_state,-2,0)
            elif input == "U":
                rock_destination_index = move_cartesian(player_index,0,-2)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,brane_state,0,-2)
            elif input == "R":
                rock_destination_index = move_cartesian(player_index,2,0)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,brane_state,2,0)
            
            rock_destination_land_value = get_land_value_from_tile(rock_destination_tile_value)
            rock_destination_rock_value = get_rock_value_from_tile(rock_destination_tile_value)
            
            # Player does a push.
            if floating(brane_state):
                print("Error! Death by wing pushing??")
                death_flag = True
                return "death"
            else:
                brane_state[player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data)
            
            # If this is a wall or another rock, it can't move.
            if rock_destination_land_value == wall_value or rock_destination_rock_value == rock_present_value:
                pass
            # Otherwise, the rock can move.
            else:
                # Moved from glass
                if moving_land_data == glass_value:
                    if moving_tile_index == -1:
                        error = input("1moving_tile_index == -1 and was attempted to be used as an index")
                    brane_state[moving_tile_index] = 0
                # Leave identical land behind.
                else:
                    if moving_tile_index == -1:
                        error = input("2moving_tile_index == -1 and was attempted to be used as an index")
                    brane_state[moving_tile_index] = create_tile_data(0, 0, moving_land_data)
                    
                ## This code automatically deals with killing enemies.
                
                # Moving into a pit, do nothing.
                if rock_destination_land_value == void_value:
                    pass
                # Moving onto a white tile, glass, or stairs.
                elif rock_destination_land_value == white_value or rock_destination_land_value == glass_value or rock_destination_land_value == exit_value:
                    brane_state[rock_destination_index] = create_tile_data(rock_entity_type, rock_present_value, rock_destination_land_value)
                # Moving onto an inactive chain tile.
                elif rock_destination_land_value == chain_inactive_value:
                    brane_state[rock_destination_index] = create_tile_data(rock_entity_type, rock_present_value, chain_active_value)
                # Moving onto an ACTIVE chain tile.
                elif rock_destination_land_value == chain_active_value:
                    trigger_chain_disperse(brane_state, rock_destination_index)
                    
                    if get_player_index(brane_state, handling_absent_case=True) == -1:
                        print("Error! Death by remote chain dispersion??")
                        death_flag = True
                        return
                # Unhandled tile type.
                else:
                    error = input("Error! Cannot resolve world state!1 " + input + " " + str(rock_destination_land_value))
                    return "???"
        else:
            # Update glass and chain counters.
            if (moving_land_data == glass_value):
                steps_since_last_glass = 0
            elif (moving_land_data == chain_inactive_value or moving_land_data == chain_active_value):
                steps_since_last_chain = 0

            # Tile we're moving into is a pit. (Or an active chain, which is similar.)
            if moving_land_data == void_value or moving_land_data == chain_active_value:
                # Moving into a pit is a death sentence.
                if not wings or (wings and floating(brane_state)):
                    # Remove player from source tile
                    if player_land_data == glass_value:
                        brane_state[player_index] = void_value
                    else:
                        brane_state[player_index] = create_tile_data(0, 0, player_land_data)
                    
                    # If the tile we're moving into is an active chain, trigger a dispersion.
                    if moving_land_data == chain_active_value:
                        if moving_tile_index == -1:
                            error = input("3moving_tile_index == -1 and was attempted to be used as an index")
                        trigger_chain_disperse(brane_state, moving_tile_index)
                    
                    # Final check to see if the brand is carved by this final action.
                    if not is_brand_carved(brane_state, brand_dicts[chosen_brand]):
                        print("Error! Death by pit??")
                        death_flag = True
                        return
                # nah bro we good I got wings and I'm not floating either
                else:
                    # Remove player from source tile
                    if player_land_data == glass_value:
                        brane_state[player_index] = void_value
                    else:
                        brane_state[player_index] = create_tile_data(0, 0, player_land_data)
                    
                    # Disperse chains
                    if moving_land_data == chain_active_value:
                        if moving_tile_index == -1:
                            error = input("4moving_tile_index == -1 and was attempted to be used as an index")
                        trigger_chain_disperse(brane_state, moving_tile_index)
                    
                    # Add player to destination tile
                    if moving_tile_index == -1:
                        error = input("5moving_tile_index == -1 and was attempted to be used as an index")
                    brane_state[moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), 0)
            # Tile is a solid tile, glass, chain, or walkable stairs.
            elif moving_land_data == white_value or moving_land_data == glass_value or moving_land_data == chain_inactive_value or (moving_land_data == exit_value and not stairs_exitable_question(brane_state)):
                steps_since_last_bump += 1
                
                # Remove player from source tile
                if player_land_data == glass_value:
                    brane_state[player_index] = void_value
                else:
                    brane_state[player_index] = create_tile_data(0, 0, player_land_data)
                    
                # Add player to destination tile
                if moving_land_data == chain_inactive_value:
                    if moving_tile_index == -1:
                        error = input("6moving_tile_index == -1 and was attempted to be used as an index")
                    brane_state[moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), chain_active_value)
                else:
                    if moving_tile_index == -1:
                        error = input("7moving_tile_index == -1 and was attempted to be used as an index")
                    brane_state[moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), moving_land_data)
            # Tile we're moving into is active stairs.
            elif moving_land_data == exit_value and stairs_exitable_question(brane_state):
                print("Error! Death by stairs??")
                death_flag = True
                return "death"
            # Tile is a wall. This is basically the same as solid tile except we only change the facing direction.
            elif moving_land_data == wall_value:
                steps_since_last_bump = 0
                
                if floating(brane_state):
                    print("Error! Death by wing pushing??")
                    death_flag = True
                return "death"
                
                brane_state[player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data)
            else:
                error = input("Error! Cannot resolve world state!2 " + input)
        return "???"
    else:
        error = input("Error! Cannot resolve world state!3 " + input)
        return "???"

## The dictionaries! ##
player_down_solid = create_tile_data(1, 1, white_value)
player_down_glass = create_tile_data(1, 1, glass_value)

mimic_down_glass = create_tile_data(mimic_entity_type, 1, glass_value)

rockless_button = create_tile_data(0, 0, button_value)
rock_on_land = create_tile_data(rock_entity_type, rock_present_value, white_value)
hand_on_glass = create_tile_data(rock_entity_type, hands_present_value, glass_value)
rock_on_glass = create_tile_data(rock_entity_type, rock_present_value, glass_value)

brane_dicts = {
    "add": [
        white_value, void_value, void_value, exit_value, void_value, white_value,
        void_value, void_value, void_value, white_value, white_value, void_value,
        void_value, white_value, white_value, white_value, white_value, white_value,
        white_value, white_value, player_down_solid, white_value, white_value, void_value,
        void_value, white_value, white_value, void_value, void_value, void_value,
        white_value, void_value, void_value, void_value, void_value, white_value,
    ],
    "eus": [
        glass_value, glass_value, glass_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, player_down_solid, white_value, glass_value, glass_value,
        glass_value, glass_value, white_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, void_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, exit_value, glass_value, wall_value,
    ],
    ## Beaver not yet impleme... bee. BEEver. Oh my god I just got that.
    "bee": [
        void_value, void_value, white_value, white_value, white_value, void_value,
        void_value, white_value, white_value, void_value, white_value, white_value,
        void_value, white_value, void_value, void_value, void_value, white_value,
        void_value, create_tile_data(beaver_entity_type, 1, exit_value), void_value, player_down_solid, white_value, void_value,
        white_value, void_value, void_value, void_value, white_value, white_value,
        wall_value, white_value, white_value, white_value, white_value, void_value,
    ],
    ## Buttons are irrelevant for this SHIT WAIT NO THEY'RE NOT IF THE STAIRS ARE INACTIVE.,..,
    ## Corner rocks are treated as walls because that's what they are.
    "mon": [
        rockless_button, white_value, white_value, white_value, white_value, wall_value,
        white_value, glass_value, glass_value, glass_value, glass_value, white_value,
        white_value, glass_value, white_value, glass_value, glass_value, white_value,
        white_value, glass_value, glass_value, player_down_solid, glass_value, white_value,
        white_value, glass_value, glass_value, glass_value, rock_on_glass, white_value,
        wall_value, white_value, white_value, white_value, white_value, exit_value,
    ],
    ## This is spaghetti
    "tan": [
        rock_on_land, hand_on_glass, player_down_solid, white_value, hand_on_glass, rock_on_land,
        hand_on_glass, hand_on_glass, white_value, white_value, hand_on_glass, hand_on_glass,
        rock_on_land, hand_on_glass, rock_on_land, rock_on_land, hand_on_glass, rock_on_land,
        white_value, white_value, exit_value, hand_on_glass, white_value, white_value,
        white_value, hand_on_glass, rock_on_land, white_value, hand_on_glass, white_value,
        white_value, white_value, hand_on_glass, hand_on_glass, white_value, white_value,
    ],
    "gor": [
        mimic_down_glass, glass_value, white_value, white_value, glass_value, player_down_glass,
        glass_value, glass_value, white_value, white_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, glass_value, glass_value, white_value,
        white_value, glass_value, glass_value, glass_value, glass_value, rock_on_land,
        glass_value, glass_value, white_value, white_value, glass_value, glass_value,
        wall_value, glass_value, white_value, white_value, glass_value, exit_value,
    ],
    "lev": [
        wall_value, chain_inactive_value, chain_inactive_value, exit_value, white_value, player_down_solid,
        chain_inactive_value, chain_inactive_value, white_value, white_value, white_value, white_value,
        white_value, chain_inactive_value, chain_inactive_value, rock_on_land, chain_inactive_value, chain_inactive_value,
        chain_inactive_value, chain_inactive_value, white_value, white_value, chain_inactive_value, chain_inactive_value,
        chain_inactive_value, chain_inactive_value, chain_inactive_value, chain_inactive_value, chain_inactive_value, white_value,
        wall_value, white_value, chain_inactive_value, chain_inactive_value, white_value, white_value
    ],
    "cif": [
        wall_value, white_value, void_value, void_value, void_value, wall_value,
        void_value, white_value, void_value, white_value, void_value, white_value,
        void_value, white_value, void_value, void_value, white_value, void_value,
        white_value, void_value, white_value, void_value, void_value, void_value,
        white_value, void_value, void_value, player_down_solid, void_value, void_value,
        wall_value, white_value, void_value, void_value, void_value, wall_value,
    ],
    #dis
}

######

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
    ],
    "developer": [
        1, 1, 0, 0, 0, 1,
        1, 0, 1, 0, 0, 1,
        1, 0, 0, 1, 1, 0,
        0, 1, 1, 0, 0, 1,
        1, 0, 0, 1, 0, 1,
        1, 0, 0, 0, 1, 1,
    ],
}

#######

def combo_name():
    return chosen_brane+"+"+chosen_brand

def combo_name_full():
    return combo_name()+"+"+str(wings)+"+"+str(sword)+"+"+str(endless)

# This should be where our focus is.
unproven_solutions = {
    "eus+add",
    "eus+bee",
    "eus+tan",
    "eus+trailer",
    "eus+dev",
    "lev+dev",
}

# ONLY used for testing.
known_solutions = {
    "add+add": "URUZ",
    
    "eus+eus": "LZRURDRLLRZRZLLRZRDLZDZDZLDR",
    "eus+lev": "LZURRDLZLRZDDUUDZDDZURUZLDUZDZDLZRZULZRUZDZULRZRRZLLRZRLZUDZDRZLUZDDZRU",
    "eus+cif": "LZRRLZDLZRRLZUUDZRUDZDZUZRLZDZRZLZDUZDZDZRRUZLLUDZUZUZDDLRZUUDZUZURLDDUZDZDUZDZDLZRUUZDDUZDZDLRZUUZDZURLZLLRZURZRZ",
    # Sum[Divide[\(40)35+1\(41)!,\(40)\(40)2+b\(41)! * 3! * \(40)30-b\(41)! * 1!\(41)]* \(40)3+30-b\(41) * 4,{b,0,33-15}]
    
    "mon+eus": "UUZLDDUZUZLRZRRZLLDZDDDRRZLUULUURLZLZDLDDRDRRRZLZRRUUULZLZDZDZUUULLUDZRRDZULLDLRZRZLDZLURZUDZDUZ",
    
    "lev+lev": "LZRDDLDRDLLDLULLURURUULDLDU",
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
soft_predestination = False
predestination_mode = False

# Define here, clear when applicable.
bad_solutions = []
bad_solutions_distance = []
current_brane_layout = []
held_tiles = []
last_trimmed = -1
move_chances = []
move_thresholds = []
moving_loops = 0
#failed_loops_distance = {}
steps_since_last_glass = 0
steps_since_last_bump = 0
steps_since_last_chain = 0
trimmings = []
working_moves = ""

while True:
    print("\n")
    if not predestination_mode and soft_predestination:
        soft_predestination = False
    elif soft_predestination:
        print("CURRENTLY IN soft PREDESTINATION MODE!!!")
    elif predestination_mode:
        print("CURRENTLY IN PREDESTINATION MODE!!!")
    print("WINGS: "+str(wings)+"\n"+"SWORD: "+str(sword)+"\n"+"ENDLESS: "+str(endless))
    
    chosen_brane = input("Starting brane? (You may also type wings, sword, or endless to toggle them.)\n")
    chosen_brane = chosen_brane.lower()
    
    if chosen_brane == "wings":
        wings = not wings
        continue
    if chosen_brane == "sword":
        sword = not sword
        continue
    if chosen_brane == "endless":
        endless = not endless
        continue
    if chosen_brane == "pred" or chosen_brane == "predestination":
        predestination_mode = not predestination_mode
        continue
    if chosen_brane == "brane":
        import time
        stopwatch = time.time()
        x = 0
        while x < 100:
            print(display_brane(random_brane()))
            x += 1
        print(str(time.time() - stopwatch))
        notice = input("Made a bunch for ya, boss.")
        
    chosen_brand = input("...And the brand?\n")
    chosen_brand = chosen_brand.lower()
    
    if chosen_brand == "dev":
        chosen_brand = "developer"

    if chosen_brane not in brane_dicts or chosen_brand not in brand_dicts:
        print("Invalid inputs. Try again.")
        continue
    elif count_valids(brand_dicts[chosen_brand]) > count_valids(brane_dicts[chosen_brane]):
        print("Target brand has more tiles than the selected brane does. This will never work!")
        continue
    elif not endless and count_valids(brand_dicts[chosen_brand]) < count_state_1s(brane_dicts[chosen_brane]):
        print("Target brand has less tiles than the selected brane does, we do not have the endless void rod, and there are not enough glass tiles to compensate. This will never work!")
        continue
    elif chosen_brand == "dis" and not brane_has_breakable_question(brane_dicts[chosen_brane]):
        print("Attempting to carve the DIS brand, but the selected brane has no glass, meaning the best we could ever do is 1 lone tile. This will never work!")
        continue
        
    if sword and not here_be_monsters_question(brane_dicts[chosen_brane]):
        print("Sword is enabled but there are no monsters. Disabling for irrelevancy.")
    
    flag = False
    for i in range(36):
        if brane_dicts[chosen_brane][i] == wall_value and brand_dicts[chosen_brand][i] == void_value:
            flag = True
            break
    if flag:
        print("Target brand has an empty space where the brane has a wall. This will never work!")
        continue
    
    # Resets this as irrelevant.
    if predestination_mode and not (combo_name() in known_solutions):
        print("Brane/brand combination not in solution list, disabling predestination mode.")
        predestination_mode = False
    
    solution_loop_counter = 0
    working_moves = ""
    bad_solutions.clear()
    bad_solutions_distance.clear()
    weirdo_flag = False
    
    cache_location = "bad_solutions/"+combo_name_full()+".txt"
    # Attempt to read the cache.
    try:
        with open(cache_location, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
            if len(lines) == 0:
                pass
            elif len(lines) % 2 != 0:
                error = input("Cache is fucked the hell up.")
            else:
                # Read and filter
                for i in range(len(lines)):
                    if i % 2 == 0:
                        if combo_name() in known_solutions and known_solutions[combo_name()].startswith(lines[i].strip()):
                            pass
                        else:
                            bad_solutions.append(lines[i].strip())
                    else:
                        if combo_name() in known_solutions and known_solutions[combo_name()].startswith(lines[i-1].strip()):
                            pass
                        else:
                            bad_solutions_distance.append(int(lines[i].strip()))
    except FileNotFoundError:
        print("No cache found.")
    
    while True:
        # Iteration
        solution_loop_counter += 1
        print("Solution loop: " + str(solution_loop_counter))
        
        # Clearings
        held_tiles.clear()
        last_trimmed = -1
        move_chances.clear()
        move_thresholds.clear()
        moving_loops = 0
        #failed_loops_distance.clear()
        steps_since_last_glass = 0
        steps_since_last_bump = 0
        steps_since_last_chain = 0
        trimmings.clear()
        
        if working_moves != "":
            #if len(bad_solutions) > 0 and working_moves == bad_solutions[-1]:
            #    print("Solution finder has generated the exact same (wrong) sequence of inputs twice in a row. This nearly-certainly implies a bug.")
            
            # Check for duplicates.
            if working_moves not in bad_solutions:
                bad_solutions.append(working_moves)
                print("Calculating distance from Heaven...")
                bad_solutions_distance.append(distance_from_heaven(current_brane_layout,brand_dicts[chosen_brand]))
                print("Calculated distance from Heaven.")
            
            # Writing to cache.
            with open(cache_location, "w", encoding="utf-8") as f:
                if len(bad_solutions) != len(bad_solutions_distance):
                    error = input("Bad solutions arrays not same length fuck it all burn it down")
                
                for i in range(len(bad_solutions) + len(bad_solutions_distance)):
                    if i % 2 == 0:
                        f.write(bad_solutions[int(i/2)]+"\n")
                    else:
                        f.write(str(bad_solutions_distance[int(i/2)])+"\n")
                    
            # I SPENT 1 AND A HALF HOURS TRYING TO FIGURE OUT WHY ASSIGNMENTS WEREN'T WORKING BECAUSE APPARENTLY WHEN YOU ASSIGN THE VARIABLE AS THE KEY, CHANGING THE VARIABLE CHANGES THE KEY AND ASSIGNING AGAIN JUST OVERRIDES WHAT WAS THERE INSTEAD OF JUST LOGGING IT AS THE NEW VALUE. I HATE DATA DICTIONARIES IN PYTHON. HATE. HATE. HATE. LET ME TE
            #failed_loops_distance[bad_solutions[-1]] = distance_from_heaven(current_brane_layout,brand_dicts[chosen_brand])
            
        working_moves = ""
        current_brane_layout.clear()
        current_brane_layout = list(brane_dicts[chosen_brane])
        
        # Soft predestination mode only kicks in after X iterations, to give better odds-reporting.
        if soft_predestination:
            predestination_mode = solution_loop_counter >= 20

        ## Try random moves until we get there!
        death_flag = False
        while True:
            moving_loops += 1
            
            if not endless and len(held_tiles) > 1:
                error = input("Endless Void Rod is not enabled but length of held_tiles array is > 1.")
            
            ## Did we do it?
            if is_brand_carved(current_brane_layout, brand_dicts[chosen_brand]):
                break
            
            print("Current moves: " + str(working_moves) + " while holding " + str(held_tiles))
            print(display_brane(current_brane_layout))
            print(count_valids(current_brane_layout))
            
            ## Special failure states
            def special_failure_states(brane_state):
                print("Checking special failures.")
                # Breakables can't be broken...
                if count_valids(brane_state)+held_valids() == count_valids(brand_dicts[chosen_brand]):
                    # No chain tiles.
                    flag = False
                    for i in range(36):
                        if get_land_value_from_tile(brane_state[i]) == chain_inactive_value:
                            flag = True
                            break
                    
                    if not flag:
                        # The brand isn't carved...
                        if not is_brand_carved(brane_state,brand_dicts[chosen_brane]):
                            # No wings...
                            if not wings:
                                # Not holding a solid tile...
                                if not (white_value in held_tiles) and not (not stairs_exitable_question(brane_state) and (exit_value in held_tiles)):
                                    # There exists no 3-line for the player to traverse with.
                                    if not three_line_present_strict(brane_state):
                                        print("Unrecoverable situation: no 3 line and glass can't be broken.")
                                        return True
                
                # Cornered.
                if not wings or floating(brane_state):
                    # Surrounded, surrounded, surrounded, surrounded.
                    if get_down_tile_land_value(brane_state) == void_value or get_down_tile_land_value(brane_state) == wall_value:
                        if get_left_tile_land_value(brane_state) == void_value or get_left_tile_land_value(brane_state) == wall_value:
                            if get_up_tile_land_value(brane_state) == void_value or get_up_tile_land_value(brane_state) == wall_value:
                                if get_right_tile_land_value(brane_state) == void_value or get_right_tile_land_value(brane_state) == wall_value:
                                    # Facing the corner or facing a pit without anything to place.
                                    faced_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state))
                                    if faced_tile_land_value == wall_value or (faced_tile_land_value == void_value and len(held_tiles) == 0):
                                        return True

            
            if special_failure_states(current_brane_layout):
                death_flag = True
                break
            
            ## YOUR TAKING TOO LONG
            if not here_be_monsters_question(brane_dicts[chosen_brane]):
                print("Trimming down repetitive movements...")
                
                # High-level theft of a Nintendo console.
                # ...It's just shorthand for some counters.
                def gbc_gt(x):
                    return steps_since_last_glass > x and steps_since_last_bump > x and steps_since_last_chain > x
                
                # Pickup, turn 180 degrees, and place right where it was before.
                if len(working_moves) >= 5 and gbc_gt(5) and working_moves[-5] == working_moves[-2] and working_moves[-4] == "Z" and working_moves[-3] == opposite_direction(working_moves[-2]) and working_moves[-1] == "Z":
                    if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == [working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]]:
                        print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                        death_flag = True
                        break
                    if predestination_mode:
                        error = input("Trimming occurred in predestined choices.")
                    
                    last_trimmed = moving_loops
                    trimmings.append([working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]])
                    
                    working_moves = working_moves[:-4]
                # Start facing a direction, go opposite, then go right back to facing the same way.
                if len(working_moves) >= 3 and gbc_gt(3) and working_moves[-1] == working_moves[-3] and working_moves[-2] == opposite_direction(working_moves[-1]):
                    if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == [working_moves[-2],working_moves[-1]]:
                        print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                        death_flag = True
                        break
                    if predestination_mode:
                        error = input("Trimming occurred in predestined choices.")
                    
                    last_trimmed = moving_loops
                    trimmings.append([working_moves[-2],working_moves[-1]])
                    
                    working_moves = working_moves[:-2]     
                # spin in a dizziful bliss
                if len(working_moves) >= 5 and gbc_gt(5):
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
                        if predestination_mode:
                            error = input("Trimming occurred in predestined choices.")
                            
                        last_trimmed = moving_loops
                        trimmings.append([working_moves[-4],working_moves[-3],working_moves[-2],working_moves[-1]])
                        
                        working_moves = working_moves[:-4]
                # Short stupids
                if len(working_moves) >= 3 and gbc_gt(3):
                    store = [working_moves[-3],working_moves[-2],working_moves[-1]]
                    loops = [
                        # Some Add/Add solutions do this.
                        ["D","U","U"],
                        ["U","D","D"],
                        ["L","R","R"],
                        ["R","L","L"],
                    ]
                    
                    if store in loops:
                        if len(trimmings) > 2 and trimmings[-1] == trimmings[-2] and trimmings[-1] == store:
                                print("Error! Trimming same sequence thrice in a row, likely infinite loop!")
                                death_flag = True
                                break
                        if predestination_mode:
                            error = input("Trimming occurred in predestined choices.")
                            
                        last_trimmed = moving_loops
                        trimmings.append(list(store))
                        
                        working_moves = working_moves[:-3]
                        working_moves += (store[-1])
            
                if last_trimmed == moving_loops:
                    print("Trimming complete.")
                else:
                    print("Trimming complete without doing anything.")
            
            too_long = False
            if combo_name() in known_solutions and len(working_moves) > len(known_solutions[combo_name()]):
                print("Working moves too long. Resetting...")
                death_flag = True
                too_long = True
                break
            elif len(working_moves) > 250:
                print("Working moves too long. Resetting...")
                death_flag = True
                too_long = True
                break
            elif count_valids(brand_dicts[chosen_brand]) > count_valids(current_brane_layout)+held_valids():
                print("Target brand has more tiles than the current brane state. This will never work!")
                death_flag = True
                break

            # Every so often, perform a sanity check to make sure something hasn't gone totally wrong.
            if (not brane_has_breakable_question(brane_dicts[chosen_brane]) and len(working_moves) % 1 == 0):
                default_solids = count_valids(brane_dicts[chosen_brane])
                current_solids = count_valids(current_brane_layout)

                if default_solids != current_solids + held_valids():
                    print("Sanity check fucking failed!!")
                    print("Default brane state: ", default_solids)
                    print(display_brane(brane_dicts[chosen_brane]))
                    print("Current state: ",current_solids + held_valids())
                    print(display_brane(current_brane_layout))
                    error = input("")

            ## Update glass & chain counter.
            player_index = get_player_index(current_brane_layout)
            player_land_data = get_land_value_from_tile(current_brane_layout[player_index])
            
            if (player_land_data == glass_value):
                steps_since_last_glass = 0
            else:
                steps_since_last_glass += 1
                
            if (player_land_data == chain_inactive_value or player_land_data == chain_active_value):
                steps_since_last_chain = 0
            else:
                steps_since_last_chain += 1

            ## Check for safe choices.
            #print("penis cock balls penis!!")
            safe_choices = safe_choice_list(current_brane_layout)
            #print("pussy vagina!!")

            ## No safe choices!
            if len(safe_choices) == 0:
                print("No safe choices... resetting...")
                death_flag = True
                break
            else:
                print("Choices are: ",safe_choices)
            
            ## First we establish the cache.
            threshold_cache = {}
            for choice in safe_choices:
                threshold_cache[choice] = threshold_from_choice(current_brane_layout,choice)
            
            ## Via weighted randomness, chose a move.
            current_move = ""
            while current_move == "":
                for choice in safe_choices:
                    threshold = threshold_cache[choice]
                    
                    # Special case to discourage looping
                    #if moving_loops - last_trimmed < 5 and len(trimmings) > 0 and trimmings[-1][-1] == choice:
                    #    threshold = 0
                    
                    if random.random() > threshold:
                        # Calculate chance of this specific choice being made out of all the others.
                        # Modified the safe_choices to use a sorted list instead of a set so we can know the order they come in, making the math more feasible to make accurate.
                        # Add the odds of it happening first loop plus the odds of it happening second loop etc. etc. until gains are negligible.
                        
                        non_predestined = safe_choice_list(current_brane_layout,True)
                        non_predestined_thresholds = []
                        
                        for thing in non_predestined:
                            non_predestined_thresholds.append(threshold_from_choice(current_brane_layout,thing))
                        
                        iteration_of_predestination = non_predestined.index(choice)
                        
                        def odds_iteration_machine(iterations):
                            sub_odds = 1
                            
                            for i in range(len(non_predestined)*iterations):
                                # The exact searched. Multiply by odds of happening.
                                if i == iteration_of_predestination + len(non_predestined)*iterations:
                                    sub_odds *= 1-non_predestined_thresholds[i % len(non_predestined)]
                                    break
                                # Otherwise, multiply by odds of not happening. (Random needs to be >= threshold to return True, meaning threshold is the odds of it not happening.)
                                else:
                                    sub_odds *= non_predestined_thresholds[i % len(non_predestined)]
                        
                            if sub_odds < 0:
                                error = input("Sub odds is negative. "+str(sub_odds))
                            elif sub_odds > 1:
                                error = input("Sub odds is above 1. "+str(sub_odds))
                        
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
                        if len(non_predestined) == 1:
                            odds = 1.0
                        
                        move_thresholds.append(round(threshold,3))
                        move_chances.append(round(odds,6))
                        
                        current_move = choice
                        break
            
            ## Apply the move to the list.
            working_moves += current_move

            ## Update the brane state.
            brane_walk(current_brane_layout, current_move)
            if death_flag:
                break

            ## Did we do it?
            if is_brand_carved(current_brane_layout, brand_dicts[chosen_brand]):
                break

        # We died, restart!
        if death_flag:
            if not too_long and debug_deaths:
                error = input("Why did we die?")
                
            if predestination_mode:
                error = input("Died in predestination mode.")
                
            continue
        
        break

    # We succeeded! Print the result and hang.
    print(display_brane(current_brane_layout))
    print(working_moves)
    if len(move_thresholds) != 0 and len(move_chances) != 0:
        print("Threshold (weight) for each move (higher means lower odds): "+str(move_thresholds))
        if predestination_mode:
            print("Approximate chances each move would've had in regular mode: "+str(move_chances))
        else:
            print("Approximate chances each move had: "+str(move_chances))
        
        mult_chance = 1
        
        for chance in move_chances:
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
        flag = False
        while not flag:
            if p <= 0:
                break
                
            try:
                j = math.log(1-(p/100))/math.log(1-x)
                flag = True
            except:
                p -= 1
        
        if p == 0:
            print("Oh my godddd like, the chance of succeeding is so small the floating point math rounds it down to zero lolz. So embarrassing.")
        else:
            print("It would take "+str(j)+" iterations for there to be a >"+str(p)+"% chance of finding the solution.")
            print("If each solution-length attempt took 0.1 second, this would in principle take "+str((j*0.1)/60)+" minutes to find.")
    if soft_predestination and not weirdo_flag:
        print(bad_solutions)
        print(bad_solutions_distance)
        if len(bad_solutions) != len(bad_solutions_distance):
            print("Bad solutions arrays are desynced. It sure would be nice if Python let me use a fucking dictionary for this.")
        if solution_loop_counter-1 != len(bad_solutions):
            print("Looped more times than bad_solutions entries. Bug!")
        
        print("Soft predestination warning: the weirdo_flag was never triggered, meaning past learning has no effect on the thresholds displayed here.")
    if not predestination_mode:
        print("THIS IS NOT PREDESTINATION MODE!!!!!!")
    blargh = input("Success! Found this route for " + chosen_brane + " brane carving " + chosen_brand)