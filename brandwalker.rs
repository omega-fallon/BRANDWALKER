// Better Rust code, go? //

// Tile setup //
const stupid_display_crap : bool = false;

const base_value : u16 = 8;
const base_value_2 : u16 = base_value*base_value;

const bits_per_variable : u16 = 3;

const player_entity_type: u16 = 0b001;
const beaver_still_entity_type: u16 = 0b010;
const beaver_charge_entity_type: u16 = 0b010;
const mimic_entity_type: u16 = 0b011;
const rock_entity_type: u16 = 0b100;

const rock_present_value: u16 = 0b001;
const monster_statue_value: u16 = 0b010;
const watcher_statue_inactive_value: u16 = 0b011;
const watcher_statue_active_value: u16 = 0b100;
const hands_present_value: u16 = 0b101;

const void_value: u16 = 0b000;
const white_value: u16 = 0b001;
const glass_value: u16 = 0b010;
const chain_inactive_value: u16 = 0b011;
const chain_active_value: u16 = 0b100;
const button_value: u16 = 0b101;
const exit_value: u16 = 0b110;
const wall_value: u16 = 0b111;

const fn create_tile_data(entity_type: u16, entity_value: u16, land: u16) -> u16 {
    if entity_type > base_value-1 || entity_value > base_value-1 || land > base_value-1 {
        panic!("Error! Invalid inputs in create_tile_data()!");
    }

    // New data structure {
    // 3rd slot - entity type (unspecified, player, beaver, mimic, rock/hand)
    // 2nd slot - entity value (not there, down, left, up, right); for rock (no rock, yes rock, greed, watcher, hands (hands!))
    // 1st slot - land tiles value (pit, solid, glass, chain inactive, chain active, button, exit, wall)
    return ((entity_type << (bits_per_variable*2)) | (entity_value << bits_per_variable) | land) as u16;
}

// Given a tile value, extracts the entity type value.
fn get_entity_type_from_tile(x: u16) -> u16 {
    return x >> bits_per_variable*2;
}

// Given a tile value, extracts the rock value.
fn get_rock_value_from_tile(mut x: u16) -> u16 {
    if get_entity_type_from_tile(x) != rock_entity_type {
        return 0;
    }
        
    x -= base_value_2*rock_entity_type;
    return x >> bits_per_variable;
}

// Given a tile value, extracts the mimic value.
fn get_mimic_value_from_tile(mut x: u16) -> u16 {
    if get_entity_type_from_tile(x) != mimic_entity_type {
        return 0;
    }
        
    x -= base_value_2*mimic_entity_type;
    return x >> bits_per_variable;
}
    
// Given a tile value, extracts the beaver value.
fn get_beaver_value_from_tile(mut x: u16) -> u16 {
    if get_entity_type_from_tile(x) != beaver_still_entity_type && get_entity_type_from_tile(x) != beaver_charge_entity_type {
        return 0;
    }
    
    x -= base_value_2*get_entity_type_from_tile(x);
    return x >> bits_per_variable;
}

// Given a tile value, extracts the player value.
fn get_player_value_from_tile(mut x: u16) -> u16 {
    if get_entity_type_from_tile(x) != 1 {
        return 0;
    }
        
    x -= base_value_2;//*1
    return x >> bits_per_variable;
}
    
// Given a tile value, extracts the land value.
fn get_land_value_from_tile(mut x: u16) -> u16 {
    while x >= base_value_2 {
        x -= base_value_2;
    }
    while x >= base_value {
        x -= base_value;
    }
    return x;
}

// The dictionaries! //
const player_down_solid : u16 = create_tile_data(1, 1, white_value);
const player_down_glass : u16 = create_tile_data(1, 1, glass_value);

const mimic_down_glass : u16 = create_tile_data(mimic_entity_type, 1, glass_value);

const rockless_button : u16 = create_tile_data(0, 0, button_value);
const rock_on_land : u16 = create_tile_data(rock_entity_type, rock_present_value, white_value);
const hand_on_glass : u16 = create_tile_data(rock_entity_type, hands_present_value, glass_value);
const rock_on_glass : u16 = create_tile_data(rock_entity_type, rock_present_value, glass_value);

const monster_statue_on_land : u16 = create_tile_data(rock_entity_type, monster_statue_value, white_value);
const watcher_on_land : u16 = create_tile_data(rock_entity_type, watcher_statue_inactive_value, white_value);

const add_brane : [u16; 36] = [
    white_value, void_value, void_value, exit_value, void_value, white_value,
    void_value, void_value, void_value, white_value, white_value, void_value,
    void_value, white_value, white_value, white_value, white_value, white_value,
    white_value, white_value, player_down_solid, white_value, white_value, void_value,
    void_value, white_value, white_value, void_value, void_value, void_value,
    white_value, void_value, void_value, void_value, void_value, white_value,
];

// Your oooother functions //

fn display_brane(brane: [u16; 36], ignoring_length: bool) -> String {
    if !ignoring_length && brane.len() != 36 {
        panic!("Error! Brane with invalid length.")
    }
    
    let mut string : String = String::from("");
    
    for i in 0..brane.len() {
        let mut char_to_add = '?';
        
        if brane[i] == void_value {
            char_to_add = '_';
        }
        else if brane[i] == white_value {
            char_to_add = '█';
        }
        else if brane[i] == glass_value {
            char_to_add = '/';
        }
        else if brane[i] == exit_value {
            char_to_add = 'S';
        }
        else if brane[i] == wall_value {
            char_to_add = 'W';
        }
        else if brane[i] == chain_inactive_value {
            char_to_add = 'Θ';
        }
        else if brane[i] == chain_active_value {
            char_to_add = '•';
        }
        else if brane[i] == button_value {
            char_to_add = 'B';
        }
        
        if get_rock_value_from_tile(brane[i]) == rock_present_value {
            char_to_add = 'R';
        }
        else if get_rock_value_from_tile(brane[i]) == hands_present_value {
            char_to_add = 'H';
        }
        
        if get_player_value_from_tile(brane[i]) == 1 {
            char_to_add = 'V';
        }
        else if get_player_value_from_tile(brane[i]) == 2 {
            char_to_add = '<';
        }
        else if get_player_value_from_tile(brane[i]) == 3 {
            char_to_add = '^';
        }
        else if get_player_value_from_tile(brane[i]) == 4 {
            char_to_add = '>';
        }

        string.push_str(char_to_add);
        string.push(' ');

        if i == 5 || i == 11 || i == 17 || i == 23 || i == 29 {
            string.push('\n');
        }
    }
    
    return string
}

const max_tile_value : u16 = create_tile_data(base_value-1, base_value-1, base_value-1);
// Given a brane state && a brand, returns true if the brand is currently successfully carved.
fn is_brand_carved(brane_state: [u16; 36], brand: [bool; 36]) -> bool {
    for i in 0..36 {
        // First, validate the inputs to avoid any dumb mistakes.
        if brane_state[i] > max_tile_value {
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state, false))
        }
        
        // Now, check in earnest.
        let i_brane_state_land = get_land_value_from_tile(brane_state[i]);
        if i_brane_state_land == void_value && brand[i] == false {
            continue
        }
        else if i_brane_state_land != void_value && i_brane_state_land != exit_value && brand[i] == true {
            continue
        }
        return false
    }

    return true
}

// Given a brane state && a brand, returns true if the brand is currently successfully carved, treating stairs as void.
fn is_brand_carved_minus_stairs(brane_state: [u16; 36], brand: [bool; 36]) -> bool {
    for i in 0..36 {
        // First, validate the inputs to avoid any dumb mistakes.
        if brane_state[i] > max_tile_value {
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state, false))
        }
        
        // Now, check in earnest.
        let i_brane_state_land = get_land_value_from_tile(brane_state[i]);
        if i_brane_state_land == void_value && brand[i] == false {
            continue
        }
        else if i_brane_state_land == glass_value && get_player_value(brane[i]) != 0 && brand[i] == false {
            continue   
        }
        else if i_brane_state_land != void_value && i_brane_state_land != exit_value && brand[i] == true {
            continue
        }
        return false
    }

    return true
}
    
// Given a brane state && a brand, returns true if the brand would be successfully carved if the tile the player is currently standing on is glass && was removed.
fn is_brand_carved_minus_stood_glass(brane_state: [u16; 36], brand: [bool; 36]) -> bool {
    for i in 0..36 {
        // First, validate the inputs to avoid any dumb mistakes.
        if brane_state[i] > max_tile_value {
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state, false))
        }
        
        // Now, check in earnest.
        let i_brane_state_land = get_land_value_from_tile(brane_state[i]);
        if (i_brane_state_land == void_value || i_brane_state_land == exit_value) && brand[i] == false {
            continue;
        }
        else if i_brane_state_land != void_value && i_brane_state_land != exit_value && brand[i] == true {
            continue;
        }
        return false;
    }

    return true;
}

// Given a brane state, returns the index of the player's position.
fn get_player_index(brane_state: [u16; 36], handling_absent_case: bool) -> u16 {
    let mut store = 37;
    for i in 0..36 {
        if get_entity_type_from_tile(brane_state[i]) == player_entity_type {
            if store != 37 {
                panic!("Error! Multiple players found by get_player_index()\n"+ display_brane(brane_state))
            }
            store = i;
        }            
    }

    if store != 37 || handling_absent_case {
        return store;
    }

    panic!("Error! Player could not be found by get_player_index()!\n"+ display_brane(brane_state))
}

// Given a brane state, returns the index of the stairs.
fn get_stairs_index(brane_state: [u16; 36]) -> u16 {
    let mut store = 37;
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == exit_value {
            if store != 37 {
                panic!("Error! Multiple stairs found by get_stairs_index()!\n"+ display_brane(brane_state))
            }
            store = i
        }
    }

    if store != 37 {
        return store
    }

    panic!("Error! Stairs could not be found by get_stairs_index()!\n"+ display_brane(brane_state))
}

// Given a brane state, returns the land value of the tile the player is standing on.
fn get_player_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(brane_state[get_player_index(brane_state)])
}

// Given a brane state, returns the player's facing value.
fn get_player_direction_number(brane_state: [u16; 36]) -> u16 {
    return get_player_value_from_tile(brane_state[get_player_index(brane_state)])
}

// Given a brane state, returns the player's facing value as a letter.
const cardinals : [char; 4] = ['D', 'L', 'U', 'R'];
fn player_faced_direction_letter(brane_state: [u16; 36]) -> char {
    return cardinals[get_player_direction_number(brane_state) - 1]
}

// Given a facing letter, returns the equivalent number.
fn direction_letter_to_number(letter : char) -> u16 {
    if letter == 'D' {
        return 1
    }
    else if letter == 'L' {
        return 2
    }
    else if letter == 'U' {
        return 3
    }
    else if letter == 'R' {
        return 4
    }
    else {
        panic!("Error! No valid number equivalent for letter input in direction_letter_to_number()! " + letter);
    }        
}

// Gives the tile INDEX of the tile in front of the player. Don't call this directly unless handling -1 case.
fn index_tile_in_direction_of_player(brane_state: [u16; 36], mut player_direction: u16) {
    let player_i : u16 = get_player_index(brane_state);
    if player_direction == 0 {
        player_direction = get_player_value_from_tile(brane_state[player_i]);
    }

    if player_direction == 0 {
        panic!("Error! Player does not exist to index_tile_in_front_of_player()!")
    }
    else if player_direction == 1 { // down
        if player_i + 6 > 35 {
            return 37;
        }
        else {
            return player_i + 6;
        }
    }
    else if player_direction == 2 { // left
        if (player_i == 0 || player_i == 6 || player_i == 12 || player_i == 18 || player_i == 24 || player_i == 30) {
            return 37;
        }
        else {
            return player_i - 1;
        }
    }
    else if player_direction == 3 { // up
        if player_i - 6 < 0 {
            return 37;
        }
        else {
            return player_i - 6;
        }
    }
    else if player_direction == 4 { // right
        if (player_i == 5 || player_i == 11 || player_i == 17 || player_i == 23 || player_i == 29 || player_i == 35) {
            return 37;
        }
        else {
            return player_i + 1;
        }
    }
    else {
        panic!("Error! Player does not have valid direction to index_tile_in_direction_of_player()! "+brane_state)
    }
}

// Same as the above but returns the actual data in one step.
fn tile_in_direction_of_player(brane_state: [u16; 36], forced_direction: char) -> u16 {
    let i = index_tile_in_direction_of_player(brane_state, forced_direction);

    if i == 37 {
        return wall_value
    }
    else {
        return brane_state[i]
    }
}

// Land value convenience functions
fn get_down_tile_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,'D'))
}
fn get_left_tile_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,'L'))
}
fn get_up_tile_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,'U'))
}
fn get_right_tile_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(tile_in_direction_of_player(brane_state,'R'))
}

// Returns true if the void rod can take a file.
fn void_rod_can_take(passed_tiles: Vec<u16>) -> bool {
    return passed_tiles.len() == 0 || endless;
}

// Returns the opposite direction of the input. Returns a letter if inputted a letter && a number if inputted a number.
fn opposite_direction_letter(x: char) -> char {
    if x == 'U' {
        return 'D'
    }
    else if x == 'D' {
        return 'U'
    }
    else if x == 'L' {
        return 'R'
    }
    else if x == 'R' {
        return 'L'
    }
    else {
        return 'X'
    }
}
fn opposite_direction_number(x: u16) -> u16 {
    if x == 1 {
        return 3
    }
    else if x == 2 {
        return 4
    }
    else if x == 3 {
        return 1
    }
    else if x == 4 {
        return 2
    }
    else {
        return -1
    }
}

// Returns true if there any MOVING monsters in the brane. Because this is used to determine if turn-wasting is worthwhile, hands (hands!) are not counted.
fn here_be_moving_monsters_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if get_entity_type_from_tile(brane_state[i]) == beaver_still_entity_type || get_entity_type_from_tile(brane_state[i]) == beaver_charge_entity_type || get_entity_type_from_tile(brane_state[i]) == mimic_entity_type {
            return true
        }
    }

    return false
}
    
// Returns true if there any monsters in the brane, INCLUDING hands, hands!
fn here_be_monsters_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if get_entity_type_from_tile(brane_state[i]) == beaver_still_entity_type || get_entity_type_from_tile(brane_state[i]) == beaver_charge_entity_type || get_entity_type_from_tile(brane_state[i]) == mimic_entity_type || get_rock_value_from_tile(brane_state[i]) == hands_present_value {
            return true
        }
    }

    return false
}

// Returns true if the input brane state has any breakable tiles in it.
const breakables : [u16; 3] = [glass_value, chain_inactive_value, chain_active_value];
fn brane_has_breakable_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if breakables.contains(get_land_value_from_tile(brane_state[i])) {
            return true
        }
    }
    return false
}

// Returns true if the input brane state has an exit.
fn brane_has_stairs_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == exit_value {
            return true
        }
    }
    return false
}

// Counts brand-valid tiles.
fn count_valids_in_brane(brane_state: [u16; 36]) -> u16 {
    let mut counter : u16 = 0;
    for i in 0..36 {
        if (get_land_value_from_tile(brane_state[i]) != void_value && get_land_value_from_tile(brane_state[i]) != exit_value) {
            counter += 1
        }
    }
    return counter
}

// Counts state-1 tiles.
fn count_state_1s(brane_state: [u16; 36]) -> u16 {
    let mut counter : u16 = 0;
    for i in 0..36 {
        if (get_land_value_from_tile(brane_state[i]) == white_value) {
            counter += 1
        }
    }
    return counter
}

// Checks if the stairs are active (i.e., available to exit from)
fn stairs_exitable_question(brane_state: [u16; 36]) -> bool {
    // Check the rod first.
    if held_tiles.contains(exit_value) {
        return false
    }

    // Check the brane.
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == button_value {
            // Button doesn't have a rock on it but does have a non-player entity on it.
            if get_entity_type_from_tile(brane_state[i]) == beaver_still_entity_type || get_entity_type_from_tile(brane_state[i]) == beaver_charge_entity_type || get_entity_type_from_tile(brane_state[i]) == mimic_entity_type {
                pass
            }
            else {
                return false
            }
        }
    }

    return true
}

// Returns the number of valid tiles currently held by the wand.
fn held_valids() -> u16 {
    let mut counter : u16 = 0;
    for x in held_tiles {
        if x != 0 && x != 3 {
            counter += 1
        }
    }
    return counter
}
    
// Returns the number of valid tiles in the input list.
fn count_valids_gen(input: list) -> u16 {
    let mut counter : u16 = 0;
    for x in input {
        if x != 0 && x != 3 {
            counter += 1
        }
    }
    return counter;
}
    
// Gives a value representing the "distance" between a brane state && the solution. This is calculated as the number of mismatched tiles, NOT distance in a state-space way. What, do you think I'm competent at coding || something?
fn distance_from_heaven(brane_state: [u16; 36], brand: [bool; 36]) -> f64 {
    let mut distance : f64 = 0;
    
    // Initial conception of distance
    for i in 0..36 {
        let i_brane_state_land = get_land_value_from_tile(brane_state[i]);
        
        if i_brane_state_land == void_value && brand[i] == false {
            continue;
        }
        else if i_brane_state_land != void_value && i_brane_state_land != exit_value && brand[i] == true {
            continue;
        }
        
        distance += 1;
    }
        
    // Failure states get special penalty.
    if get_player_index(brane_state, handling_absent_case = true) == -1 {
        distance += 10;
    }
    else {
        if special_failure_states(brane_state) {
            distance += 10;
        }
        if safe_choice_list(brane_state,true).len() == 0 {
            distance += 10;
        }
    }
    
    return distance;
}
    
// Returns taxicab distance between two points on the brane room, given by their index.
fn taxicab_distance(a: u16, b: u16) -> u16 {
    let x1 = a % 6;
    let y1 = int(a/6);
    
    let x2 = b % 6;
    let y2 = int(b/6);
    
    return abs(x1 - x2) + abs(y1 - y2);
}
    
// Returns true if player is floating.
fn floating(brane_state: [u16; 36]) -> bool {
    return get_player_land_value(brane_state) == void_value
}

// Returns true if the tile is undesirable (or impossible) to move into. Takes a land value.
fn land_undesirable(land: int, brane_state: [u16; 36]) -> bool {
    return ((land == void_value || land == chain_active_value) && wings && floating(brane_state)) || ((land == void_value || land == chain_active_value) && !wings) || land == wall_value || (land == exit_value && stairs_exitable_question(brane_state))
}

// Given the state && an input, returns the predicted change in "solution distance" if the player were to take that action.
// Positive change indicates increasing distance, while negative represents lowering the distance. Thus, here, negative is desirable.
fn predicted_distance_change(brane_state: [u16; 36], input_letter: char) -> u16 {
    let mut total : i16 = 0;
    
    let brand = brand_dicts[chosen_brand];
    
    let faced_tile = tile_in_direction_of_player(brane_state);
    let faced_tile_land_value = get_land_value_from_tile(faced_tile);
    
    if input_letter == 'Z' {
        // Player is placing a tile.
        if faced_tile_land_value == void_value && held_tiles.len() != 0 {
            // Player is placing stairs.
            if held_tiles[-1] == exit_value {
                total += 1
            }
            // Player is placing a tile where the brand has a solid tile.
            else if brand[index_tile_in_direction_of_player(brane_state)] == 1 {
                total += -1
            }
            // Player is placing a tile where the brand does NOT have a solid tile.
            else {
                total += 1
            }
        }
        // Player is picking up a tile.
        else if faced_tile_land_value != void_value && faced_tile_land_value != wall_value && void_rod_can_take() {
            // Player is picking up stairs.
            if faced_tile_land_value == exit_value {
                total += -1
            }
            // Player is picking up a tile where the brand has an empty tile.
            else if brand[index_tile_in_direction_of_player(brane_state)] == void_value {
                total += -1
            }
            else {
                total += 1
            }
        }
    }
    else if input_letter == 'D' || input_letter == 'L' || input_letter == 'U' || input_letter == 'R' {
        // Standing on glass.
        if get_player_land_value(brane_state) == glass_value {
            // Tile we're moving into is moveinto-able, but not glass
            if !(faced_tile_land_value == exit_value && stairs_exitable_question(brane_state)) && faced_tile_land_value != wall_value {
                // Determine the effect of this action.
                if brand[get_player_index(brane_state)] == 0 {
                    total += -1
                }
                else {
                    total += 1
                }
            }
        }
           
        // Moving into glass
        if faced_tile_land_value == glass_value {
            if brand[index_tile_in_direction_of_player(brane_state)] == 0 {
                total += -1
            }
            else {
                total += 1
            }
        }
        // Moving onto an active chain tile.
        else if faced_tile_land_value == chain_active_value && wings && !floating(brane_state) {
            total += distance_from_heaven(trigger_chain_disperse(list(brane_state),index_tile_in_direction_of_player(brane_state,letter))) - distance_from_heaven(brane_state)
        }
                    
        // Fractional weights for moving closer to the stairs.
        if brane_has_stairs_question(brane_state) {
            total += (taxicab_distance(index_tile_in_direction_of_player(brane_state),get_stairs_index(brane_state)) - taxicab_distance(get_player_index(brane_state),get_stairs_index(brane_state))) / 3
        }
    }
            
    // What is the average distance from Heaven among all prior iterations beginning here?
    let mut total_distance = 0;
    let mut paths_matched = 0;
    
    for i in 0..bad_solutions.len() {
        let walked_path : String = bad_solutions[i];
        
        // Check if we'd go out of bounds.
        a : str = working_moves + input_letter;
        if a.len() > walked_path.len() {
            continue;
        }
        
        // See if the paths match.
        let mut flag = false;
        for i2 in 0..a.len() {
            if a[i2] != walked_path[i2] {
                break;
            }
            flag = true;
        }
            
        // Match found!
        paths_matched += 1;
        total_distance += bad_solutions_distance[i];
        
        // Slight tilt, increase perceived distance if the path is short. (Died.)
        total_distance += min(20,(20 - walked_path.len()));
    }
        
    // Average && add as factor.
    if paths_matched > 0 {
        scaling_factor = 6*6;
        total += (total_distance/paths_matched)/scaling_factor;
        
        global weirdo_flag;
        weirdo_flag = true;
        //print("THEYDIES && GENTLETHEMS, WE GOT 'EM.")
    }
        
    // Failsafe: distance is 0.
    return total;
}
    
// Based on brane state && choice, returns the threshold based on its prediction.
fn threshold_from_choice(brane_state: [u16; 36],choice) {
    // \min\left(0.95,\max\left(0.05,0.5\cdot\frac{\left(x+1.5\right)}{\left(1.5\right)}\right)\right)
    
    slant_factor = 5
    threshold = 0.5*((predicted_distance_change(brane_state,choice)+slant_factor)/slant_factor)
    
    // Clamp the threshold so that nothing is ever truly certain || impossible
    if threshold > 0.95 {
        threshold = 0.95
    }
    else if threshold < 0.05 {
        threshold = 0.05
    }
        
    return threshold
}
    
// Given an i value for a brane array && movements on the x && y axis, returns a new i index corresponding to that movement.
fn move_cartesian(i: int, x: int, y: int) {
    store = i + x + 6*y
    
    if store > 35 || store < 0 || int(i/6) != int ((i+x)/6) {
        return -1
    }
    else {
        return store
    }
}
    
// Given a starting position && cartesian movements, returns the full tile value of the tile at that index. Accounts for OOB searching.
fn tile_at_moved_cartesian(i: int, brane_state: [u16; 36], x: int, y: int) {
    store = move_cartesian(i, x, y)
    
    if store == -1 {
        return wall_value
    }
    else {
        return brane_state[store]
    }
}
    
// Given a starting position && cartesian movements, returns the land value of the tile at that index. Accounts for OOB searching.
fn land_at_moved_cartesian(i: int, brane_state: [u16; 36], x: int, y: int) {
    store = move_cartesian(i, x, y)
    
    if store == -1 {
        return wall_value
    }
    else {
        return get_land_value_from_tile(brane_state[store])
    }
}
    
// Returns true if the land value of this tile is 1 || (3, inactive).
fn effective_type_1(i: int, brane_state: [u16; 36]) {
    return (get_land_value_from_tile(i) == white_value || (get_land_value_from_tile(i) == exit_value && !stairs_exitable_question(brane_state))) && get_entity_type_from_tile(i) == 0
}
    
// Returns true if there is a 3 line of moveable land tiles. This includes only type-1 && inactive type-3.
fn three_line_present_strict(brane_state: [u16; 36]) {
    for i in 0..36 {
        
        if i + 3 <= 35 && int(i/6) == int((i+3)/6) && effective_type_1(brane_state[i],brane_state) && effective_type_1(brane_state[i+1],brane_state) && effective_type_1(brane_state[i+2],brane_state) {
            return true
        }
        if i + 6*2 <= 35 && effective_type_1(brane_state[i],brane_state) && effective_type_1(brane_state[i+6],brane_state) && effective_type_1(brane_state[i+12],brane_state) {
            return true
        }
    }
            
    return false;
}
    
// Given a brane layout && starting position, triggers a chain dispersion.
fn trigger_chain_disperse(mut brane_state: [u16; 36], i: int) -> [u16; 36] {
    if i < 0 {
        return brane_state;
    }
    
    triggered_tiles : Vec<u16> = vec![i];
    
    let mut done_something = true;
    while done_something {
        done_something = false;
        
        for triggered_i in triggered_tiles {
            // Confirm land.
            if get_land_value_from_tile(brane_state[triggered_i]) != chain_active_value {
                panic!("triggered_i isn't an active chain: "+str(triggered_i)+" "+str(triggered_tiles))
            }
                
            // Check each direction.
            if triggered_i-1 >= 0 && !triggered_tile.contains(triggered_i-1) && get_land_value_from_tile(brane_state[triggered_i-1]) == chain_active_value {
                done_something = true
                triggered_tiles.add(triggered_i-1)
                break
            }
            if triggered_i+1 <= 35 && !triggered_tile.contains(triggered_i+1) && get_land_value_from_tile(brane_state[triggered_i+1]) == chain_active_value {
                done_something = true
                triggered_tiles.add(triggered_i+1)
                break
            }
            if triggered_i-6 >= 0 && !triggered_tile.contains(triggered_i-6) && get_land_value_from_tile(brane_state[triggered_i-6]) == chain_active_value {
                done_something = true
                triggered_tiles.add(triggered_i-6)
                break
            }
            if triggered_i+6 <= 35 && !triggered_tile.contains(triggered_i+6) && get_land_value_from_tile(brane_state[triggered_i+6]) == chain_active_value {
                done_something = true
                triggered_tiles.add(triggered_i+6)
                break
            }
        }
    }
                
    // Remove the tiles.
    for triggered_i in triggered_tiles {
        if wings && get_entity_type_from_tile(brane_state[triggered_i]) == player_entity_type {
            brane_state[triggered_i] = create_tile_data(player_entity_type,get_player_value_from_tile(brane_state[triggered_i]),0)
        }
        else {
            brane_state[triggered_i] = 0;
        }
    }
    return brane_state
}
    
// Shorthand for a use case of the above.
fn trigger_chain_disperse_direction(brane_state: [u16; 36], direction) -> [u16; 36] {
    return trigger_chain_disperse(brane_state,index_tile_in_direction_of_player(brane_state,direction))
}
    
// Given a brane layout, returns the list of not-obviously-stupid inputs.
fn safe_choice_list(brane_state: [u16; 36], stupid_flaggot: bool) -> Vec<char> {
    choices = {'D', 'L', 'U', 'R', 'Z'}

    down_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 'D'))
    left_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 'L'))
    up_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 'U'))
    right_tile_land_value = get_land_value_from_tile(tile_in_direction_of_player(brane_state, 'R'))

    faced_tile = tile_in_direction_of_player(brane_state)
    faced_tile_land_value = get_land_value_from_tile(faced_tile)

    // Deadly || round-ending //
    for key, value in {'D': down_tile_land_value, 'L': left_tile_land_value, 'U': up_tile_land_value, 'R': right_tile_land_value}.items() {
        // Going down stairs.
        if value == exit_value && stairs_exitable_question(brane_state) {
            choices.remove(key)
        }
        // Falling into a pit while wingless || floating without standing on glass that's the last piece to remove before the brand is carved.
        else if value == void_value {
            if !wings || floating(brane_state) {
                if !is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand]) {
                    choices.remove(key)
                }
            }
        }
        // Stepping on an active chain while wingless || floating which wouldn't result in the brand being carved.
        else if value == chain_active_value {
            if !wings || floating(brane_state) {
                if !(value == chain_active_value && is_brand_carved(trigger_chain_disperse_direction(list(brane_state), key), brand_dicts[chosen_brand])) {
                    choices.remove(key)
                }
            }
        }
        // Breaking a piece of glass that brings total carve-valid tiles below the brand's amount.
        else if value == glass_value && count_valids_in_brane(brane_state)+held_valids() == count_valids_in_brane(brand_dicts[chosen_brand]) {
            choices.remove(key)
        }
    }
        
    // Dumb but not deadly //
    // There is no tile in front of the player && the player does not have any tile stored. There is no point in pressing 'Z'
    if faced_tile_land_value == void_value && held_tiles.len() == 0 {
        choices.remove('Z')
    }
    // There is a tile in front of the player && the player lacks the ability to take it. There is no point in pressing 'Z'
    else if faced_tile_land_value != void_value && !void_rod_can_take() {
        choices.remove('Z')
    }
    // Special case.
    else if (chosen_brand == "add" && chosen_brane == "add") || (chosen_brand == "lev" && chosen_brane == "lev") {
        if !(faced_tile_land_value == exit_value && void_rod_can_take()) {
            choices.remove('Z')
        }
    }

    // The tile in front is a wall, && there are no monsters to make wasting a turn meaningful.
    // Hitting a wall to your side CAN be useful to reposition, so we will not discount it!
    if faced_tile_land_value == wall_value && !here_be_moving_monsters_question(brane_state) && choices.contains(player_faced_direction_letter(brane_state)) {
        choices.remove(player_faced_direction_letter(brane_state))
    }
    
    // Pointless movements (repetitive ones are trimmed afterward, not outright removed) //
    if !here_be_moving_monsters_question(brane_state) {
        // Entering a dead end. (Dumb bun.)
        if !breakables.contains(get_player_land_value(brane_state)) {
            player_index = get_player_index(brane_state)
            
            for x in cardinals {
                // Don't check to see if the land is moveable; if it hasn't been removed by an earlier filter, it is.
                if !choices.contains(x) {
                    continue
                }
                
                // Confirm potential movement tile attributes && make pawn tile variables.
                if x == 'D' && !breakables.contains(down_tile_land_value) && !land_undesirable(down_tile_land_value,brane_state) {
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,2)
                }
                else if x == 'L' && !breakables.contains(left_tile_land_value) && !land_undesirable(left_tile_land_value,brane_state) {
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,-2,0)
                }
                else if x == 'U' && !breakables.contains(up_tile_land_value) && !land_undesirable(up_tile_land_value,brane_state) {
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,-1,-1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,0,-2)
                }
                else if x == 'R' && !breakables.contains(right_tile_land_value) && !land_undesirable(right_tile_land_value,brane_state) {
                    pawn_land_value_attack_1 = land_at_moved_cartesian(player_index,brane_state,1,-1)
                    pawn_land_value_attack_2 = land_at_moved_cartesian(player_index,brane_state,1,1)
                    pawn_land_value_first_turn = land_at_moved_cartesian(player_index,brane_state,2,0)
                }
                else {
                    continue
                }
                
                pawn_land_value_backwards = get_land_value_from_tile(tile_in_direction_of_player(brane_state,opposite_direction(x)))
                
                // Ignore if at the end of the "dead end" we could potentially place || pick up a tile. That makes it useful.
                if (pawn_land_value_first_turn == void_value && held_tiles.len() > 0) || (pawn_land_value_first_turn != void_value && pawn_land_value_first_turn != wall_value && void_rod_can_take()) {
                    pass
                }
                // Ignore if the tile behind the player is empty && the void rod can place, || solid && the void rod can take. This could be a useful repositioning tactic.
                else if (pawn_land_value_backwards == void_value && held_tiles.len() > 0) || (void_rod_can_take() && pawn_land_value_backwards != void_value && pawn_land_value_backwards != wall_value) {
                    pass
                }
                // Remove if dead end.
                else if land_undesirable(pawn_land_value_attack_1, brane_state) && land_undesirable(pawn_land_value_attack_2, brane_state) && land_undesirable(pawn_land_value_first_turn, brane_state) {
                    print("Pawn values found to be dead end {",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    print("Direction {",x)
                    choices.remove(x)
                }
                else {
                    pass
                    //print("Pawn values found not to be dead end {",pawn_land_value_attack_1,pawn_land_value_attack_2,pawn_land_value_first_turn)
                    //print("Direction {",x)
                }
            }
        }
    }
    
    if !here_be_moving_monsters_question(brane_state) && choices.contains('Z') {
        // Double z's are never useful without monsters
        if working_moves.len() > 0 && working_moves[-1] == 'Z' {
            choices.remove('Z')
        }
        // Trapping yourself is never worth it. (The "final stairs" case is overridden in a later block, disregard.)
        else if !wings && void_rod_can_take() && faced_tile_land_value != 0 && brane_has_stairs_question(brane_state) && int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state))+int(land_undesirable(down_tile_land_value,brane_state)) == 3 {
            choices.remove('Z')
        }
    }
    
    // Historically bad choices //
    for choice in {'D','L','U','R','Z'} {
        if bad_solutions.contains(working_moves + choice) && choices.contains(choice) {
            choices.remove(choice)
            //notice = input("We learned a lesson!! "+str(working_moves + choice)+" against "+str(choice))
        }
    }
    // Obviously correct choices //
    if !is_brand_carved(brane_state, brand_dicts[chosen_brand]) {
        // If removing the stairs is the last step && we're already facing them, always do that.
        if is_brand_carved_minus_stairs(brane_state, brand_dicts[chosen_brand]) && faced_tile_land_value == exit_value && void_rod_can_take() {
            choices = {'Z'}
        }
        // If breaking the glass we're currently on is the last step, always do that.
        else if is_brand_carved_minus_stood_glass(brane_state, brand_dicts[chosen_brand]) {
            print("Obvious choice!!")
            choices.clear()
            if down_tile_land_value == void_value || down_tile_land_value == white_value || (down_tile_land_value == exit_value && !stairs_exitable_question(brane_state)) {
                choices.add('D')
            }
            if left_tile_land_value == void_value || left_tile_land_value == white_value || (left_tile_land_value == exit_value && !stairs_exitable_question(brane_state)) {
                choices.add('L')
            }
            if up_tile_land_value == void_value || up_tile_land_value == white_value || (up_tile_land_value == exit_value && !stairs_exitable_question(brane_state)) {
                choices.add('U')
            }
            if right_tile_land_value == void_value || right_tile_land_value == white_value || (right_tile_land_value == exit_value && !stairs_exitable_question(brane_state)) {
                choices.add('R')
            }
        }
        // Dispersing chain tiles to carve the brand.
        else {
            if down_tile_land_value == chain_active_value && is_brand_carved(trigger_chain_disperse_direction(list(brane_state), 'D'), brand_dicts[chosen_brand]) {
                choices.add('D')
            }
            if left_tile_land_value == chain_active_value && is_brand_carved(trigger_chain_disperse_direction(list(brane_state), 'L'), brand_dicts[chosen_brand]) {
                choices.add('L')
            }
            if up_tile_land_value == chain_active_value && is_brand_carved(trigger_chain_disperse_direction(list(brane_state), 'U'), brand_dicts[chosen_brand]) {
                choices.add('U')
            }
            if right_tile_land_value == chain_active_value && is_brand_carved(trigger_chain_disperse_direction(list(brane_state), 'R'), brand_dicts[chosen_brand]) {
                choices.add('R')
            }
        }
    }
    
    stupid_horse = []
    for x in choices {
        stupid_horse.append(x)
    }
    
    stupid_horse.sort()
    
    // PREDESTINATION MODE //
    if !stupid_flaggot && predestination_mode {
        if burdenless() {
            predestined_choice = known_solutions_burdenless[combo_name()][working_moves.len()]
        }
        else if only_wings() {
            predestined_choice = known_solutions_wings[combo_name()][working_moves.len()]
        }
        else {
            panic!("Couldn't find predestination.")
        }
        
        if !choices.contains(predestined_choice) {
            print("Choices would've been: "+str(stupid_horse))
            panic!("Predestined choice was removed by choices algorithm. Something needs to be changed.")
        }
        
        print("Choices would've been: "+str(stupid_horse))
        
        return [predestined_choice]
    }
    
    return stupid_horse

// Given a brane layout, checks to see if there's anything that can definitively prove which brand room we're in. If it can, it returns that Void Lord's name, otherwise it returns an empty string.
fn prove_void_lord(brane_state: [u16; 36]) {
    // fill in
    
    return ""
}

// Given a brane state removes any monster statues if there are no monsters present.
fn eliminate_monster_statues(brane_state: [u16; 36]) {
    if here_be_monsters_question(brane_state) {
        for i in 0..36 {
            if get_rock_value_from_tile(brane_state[i]) == monster_statue_value {
                brane_state[i] = create_tile_data(0, 0, get_land_value_from_tile(brane_state[i]))
            }
        }
    }
    
    return brane_state
}

movement_state_dictionary = {}

// Triggers the first untriggered watcher statue found.
fn trigger_one_watcher(brane_state: [u16; 36]) {
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == watcher_statue_inactive_value {
            brane_state[i] += watcher_statue_active_value - watcher_statue_inactive_value
            return
        }
    }
    return
}

// Returns true if every watcher statue is triggered. Returns false is there are none.
fn all_watchers_triggered(brane_state: [u16; 36]) {
    any_present = false
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == watcher_statue_inactive_value {
            return false
        }
        else if get_land_value_from_tile(brane_state[i]) == watcher_statue_active_value {
            any_present = true
        }
    }
            
    return any_present
}
    
// State traversal function has a special spot right here. //
fn brane_walk(mut game_state: ([u16; 32], Vec<u16>), input: char) -> ([u16; 32], Vec<u16>) {
    global death_flag, working_moves, steps_since_last_glass, steps_since_last_bump, steps_since_last_chain
    
    // Validation.
    if !endless && game_state[1].len() > 1 {
        panic!("brane_walk passed multi-tile held without endless.")
    }
    
    // Get player index
    try {
        player_index = get_player_index(game_state[0]);
    }
    except {
        return "self";
    }
    player_land_data = get_land_value_from_tile(game_state[0][player_index])
    
    // Beaver sees player. (haven't coded excluding vision through walls, no need to)
    if chosen_brane == "bee" {
        for i in 0..36 {
            // Found inactive beaver.
            if get_entity_type_from_tile(game_state[0][i]) == beaver_still_entity_type {
                // Beaver is in LoS of player.
                if collumn_values(game_state[0], get_collumn(i)).contains(player_entity_type) || row_values(game_state[0], row_collumn(i)).contains(player_entity_type) {
                    // Set beaver facing && in charge state; makes actual movement after player.
                    if i - player_index >= 6 { // charge up.
                        game_state[0][i] = create_tile_data(beaver_charge_entity_type, 3, get_land_value_from_tile(game_state[0][i]))
                    }
                    else if player_index - i >= 6 { // charge down.
                        game_state[0][i] = create_tile_data(beaver_charge_entity_type, 1, get_land_value_from_tile(game_state[0][i]))
                    }
                    else if player_index > i { // charge right
                        game_state[0][i] = create_tile_data(beaver_charge_entity_type, 4, get_land_value_from_tile(game_state[0][i]))
                    }
                    else if player_index < i { // charge left
                        game_state[0][i] = create_tile_data(beaver_charge_entity_type, 2, get_land_value_from_tile(game_state[0][i]))
                    }
                }
                    
                // There is only one beaver. In case of scope creep, disable.
                break
            }
        }
    }
    // Player action.
    if input == 'Z' {
        full_faced_tile_data = tile_in_direction_of_player(game_state[0])
        faced_land_data = get_land_value_from_tile(full_faced_tile_data)
        
        // Slaaaaaayy the beaaast!!!
        if sword && ([beaver_still_entity_type, beaver_charge_entity_type, mimic_entity_type].contains(get_entity_type_from_tile(full_faced_tile_data)) || get_rock_value_from_tile(full_faced_tile_data) == hands_present_value) {
            game_state[0][index_tile_in_direction_of_player(game_state[0])] = create_tile_data(0,0,faced_land_data)
            game_state[0] = eliminate_monster_statues(game_state[0])
        }       
        // Is tile invalid for both pickup && placedown?
        else if full_faced_tile_data != faced_land_data || faced_land_data == wall_value { // (Explanation: this inequality means there is an entity on the tile, meaning an enemy || a rock. The second one is just checking if the tile is a wall, which is self-explanatory.) 
            return "self"
        }
        // Tile is valid for pickup.
        else if faced_land_data != void_value && faced_land_data != wall_value && void_rod_can_take(game_state[1]) {
            steps_since_last_bump += 1
            
            // Put tile on void rod.
            game_state[1].append(faced_land_data)

            // Remove the tile from the world.
            game_state[0][index_tile_in_direction_of_player(game_state[0])] = 0
            
            // Bump watcher statues.
            if chosen_brane == "lev" {
                trigger_one_watcher(game_state[0])
                if all_watchers_triggered(game_state[0]) {
                    game_state[0][player_index] = create_tile_data(0,0,player_land_data)
                    return game_state
                }
            }
        }
        // Placing tile.
        else if full_faced_tile_data == void_value && game_state[1].len() > 0 {
            steps_since_last_bump += 1
            
            // Place the tile into the world.
            game_state[0][index_tile_in_direction_of_player(game_state[0])] = game_state[1][-1]

            // Remove the tile from the void rod.
            game_state[1].pop()
            
            // Bump watcher statues.
            if chosen_brane == "lev" {
                trigger_one_watcher(game_state[0])
                if all_watchers_triggered(game_state[0]) {
                    game_state[0][player_index] = create_tile_data(0,0,player_land_data)
                    return game_state
                }
            }
        }
        // Cannot do anything.
        else {
            return "self"
        }
    }
    else if (input == 'D' || input == 'L' || input == 'U' || input == 'R') {
        moving_tile_index = index_tile_in_direction_of_player(game_state[0], direction_letter_to_number(input))

        if moving_tile_index == -1 {
            full_moving_tile_data = wall_value
            moving_land_data = wall_value
        }
        else {
            full_moving_tile_data = tile_in_direction_of_player(game_state[0], direction_letter_to_number(input))
            moving_land_data = get_land_value_from_tile(full_moving_tile_data)
        }

        // Moving into a hand (hands!)
        if get_rock_value_from_tile(full_moving_tile_data) == hands_present_value {
            return "self"
        }
        // Moving into a rock || statue.
        else if get_rock_value_from_tile(full_moving_tile_data) != 0 {
            steps_since_last_bump = 0
            
            // Determine tile the rock is moving into.
            rock_destination_index = -1
            rock_destination_tile_value = 0
            if input == 'D' {
                rock_destination_index = move_cartesian(player_index,0,2)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],0,2)
            }
            else if input == 'L' {
                rock_destination_index = move_cartesian(player_index,-2,0)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],-2,0)
            }
            else if input == 'U' {
                rock_destination_index = move_cartesian(player_index,0,-2)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],0,-2)
            }
            else if input == 'R' {
                rock_destination_index = move_cartesian(player_index,2,0)
                rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],2,0)
            }
            else {
                panic!("Unrecognized input: "+input)
            }
            
            rock_destination_land_value = get_land_value_from_tile(rock_destination_tile_value)
            rock_destination_rock_value = get_rock_value_from_tile(rock_destination_tile_value)
            
            // Player does a push.
            if floating(game_state[0]) {
                game_state[0][player_index] = void_value
            }
            else {
                game_state[0][player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data)
            }
            
            // If this is a wall || another rock, it can't move.
            if rock_destination_land_value == wall_value || (rock_destination_rock_value != 0 && rock_destination_rock_value != hands_present_value) {
                pass
            }
            // Otherwise, the rock can move.
            else {
                // Moved from glass
                if moving_land_data == glass_value {
                    if moving_tile_index == -1 {
                        panic!("1moving_tile_index == -1 && was attempted to be used as an index")
                    }
                    game_state[0][moving_tile_index] = 0
                }
                // Leave identical land behind.
                else {
                    if moving_tile_index == -1 {
                        panic!("2moving_tile_index == -1 && was attempted to be used as an index")
                    }
                    game_state[0][moving_tile_index] = create_tile_data(0, 0, moving_land_data)
                }
                    
                // This code automatically deals with killing enemies.
                
                // Moving into a pit, do nothing since the rock has already been removed from its previous tile in the last step.
                if rock_destination_land_value == void_value {
                    pass
                }
                // Moving onto a white tile, glass, stairs, || button.
                else if rock_destination_land_value == white_value || rock_destination_land_value == glass_value || rock_destination_land_value == exit_value || rock_destination_land_value == button_value {
                    game_state[0][rock_destination_index] = create_tile_data(rock_entity_type, rock_present_value, rock_destination_land_value)
                }
                // Moving onto an inactive chain tile.
                else if rock_destination_land_value == chain_inactive_value {
                    game_state[0][rock_destination_index] = create_tile_data(rock_entity_type, rock_present_value, chain_active_value)
                }
                // Moving onto an ACTIVE chain tile.
                else if rock_destination_land_value == chain_active_value {
                    trigger_chain_disperse(game_state[0], rock_destination_index)
                    game_state[0] = eliminate_monster_statues(game_state[0])
                        
                    return game_state
                }
                // Unhandled tile type.
                else {
                    panic!("Error! Cannot resolve world state!1 " + input + " " + str(rock_destination_land_value))
                    return "???"
                }
                    
                // Destroy monster statues if need be.
                game_state[0] = eliminate_monster_statues(game_state[0])
                    
                // Corner true-rocks are walls.
                if (rock_destination_index == 0 || rock_destination_index == 5 || rock_destination_index == 30 || rock_destination_index == 35) && get_rock_value_from_tile(full_moving_tile_data) == rock_present_value && get_land_value_from_tile(game_state[0][rock_destination_index]) != chain_active_value {
                    game_state[0][rock_destination_index] = wall_value
                }
            }
        }
        else {
            // Update glass && chain counters.
            if (moving_land_data == glass_value) {
                steps_since_last_glass = 0
            }
            else if (moving_land_data == chain_inactive_value || moving_land_data == chain_active_value) {
                steps_since_last_chain = 0
            }

            // Tile we're moving into is a pit. (Or an active chain, which is similar.)
            if moving_land_data == void_value || moving_land_data == chain_active_value {
                // Moving into a pit is a death sentence.
                if !wings || (wings && floating(game_state[0])) {
                    // Remove player from source tile
                    if player_land_data == glass_value {
                        game_state[0][player_index] = void_value
                    }
                    else {
                        game_state[0][player_index] = create_tile_data(0, 0, player_land_data)
                    }
                    
                    // If the tile we're moving into is an active chain, trigger a dispersion.
                    if moving_land_data == chain_active_value {
                        if moving_tile_index == -1 {
                            panic!("3moving_tile_index == -1 && was attempted to be used as an index")
                        }
                        trigger_chain_disperse(game_state[0], moving_tile_index)
                    }
                    
                    return game_state;
                }
                // nah bro we good I got wings && I'm not floating either
                else {
                    // Remove player from source tile
                    if player_land_data == glass_value {
                        game_state[0][player_index] = void_value
                    }
                    else {
                        game_state[0][player_index] = create_tile_data(0, 0, player_land_data)
                    }
                    
                    // Disperse chains
                    if moving_land_data == chain_active_value {
                        if moving_tile_index == -1 {
                            panic!("4moving_tile_index == -1 && was attempted to be used as an index")
                        }
                        trigger_chain_disperse(game_state[0], moving_tile_index)
                    }
                    // Add player to destination tile
                    if moving_tile_index == -1 {
                        panic!("5moving_tile_index == -1 && was attempted to be used as an index")
                    }
                    game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), 0)
                    }
                }
            }
            // Tile is a solid tile, glass, chain, button, || walkable stairs.
            else if moving_land_data == white_value || moving_land_data == glass_value || moving_land_data == chain_inactive_value || moving_land_data == button_value || (moving_land_data == exit_value && !stairs_exitable_question(game_state[0])) {
                steps_since_last_bump += 1
                
                // Remove player from source tile
                if player_land_data == glass_value {
                    game_state[0][player_index] = void_value
                }
                else {
                    game_state[0][player_index] = create_tile_data(0, 0, player_land_data)
                }    
                // Add player to destination tile
                if moving_land_data == chain_inactive_value {
                    if moving_tile_index == -1 {
                        panic!("6moving_tile_index == -1 && was attempted to be used as an index")
                    }
                    game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), chain_active_value)
                }
                else {
                    if moving_tile_index == -1 {
                        panic!("7moving_tile_index == -1 && was attempted to be used as an index")
                    }
                    game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), moving_land_data)
                }
            }
            // Tile we're moving into is active stairs.
            else if moving_land_data == exit_value && stairs_exitable_question(game_state[0]) {
                return "self"
            }
            // Tile is a wall. This is basically the same as solid tile except we only change the facing direction.
            else if moving_land_data == wall_value {
                steps_since_last_bump = 0
                
                if floating(game_state[0]) {
                    game_state[0][player_index] = void_value;
                    return game_state;
                }
                else {
                    game_state[0][player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data)
                    
                    // Simply changing your direction to face directly into a wall is never useful unless you're wasting a turn. If there are no moving monsters, wasting turns is pointless. Therefore we can eleminate these from the state space graph.
                    if chosen_brane == "add" || chosen_brane == "eus" || chosen_brane == "mon" || chosen_brane == "tan" || chosen_brane == "lev" || chosen_brane == "cif" || !here_be_moving_monsters_question(game_state[0]) {
                        return "fe";
                    }
                }
            }
            else {
                panic!("Error! Cannot resolve world state!2 " + input + " " + str(moving_land_data))
                return "???"
            }
        }            
    }
    else {
        panic!("Error! Cannot resolve world state!3 " + input)
        return "???"
    }
      
    // Monster turn!
    if chosen_brane == "bee" {
        for i in 0..36 {
            // Charging beaver found.
            if get_entity_type_from_tile(game_state[0][i]) == beaver_charge_entity_type {
                // Charging down
                // Charging left
                // Charging up
                // Charging right
                // fill in!
                break;
            }
        }
    }
      
    return game_state
}

fn main() {
    
    let mut held_tiles : Vec<u16> = vec![];

    println!("{}", display_brane(add_brane, false));
    println!("There is nothing.");
}