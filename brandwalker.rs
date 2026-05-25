// Better Rust code, go? //

// Config //
const chosen_brane : &str = "eus";
const chosen_brand : &str = "eus";

const wings : bool = false;
const sword : bool = false;
const endless : bool = false;

fn valids_in_brand() -> u16 {
    return count_valids_in_brand(brand_dicts.get(chosen_brand));
}
fn any_glass() -> bool {
    return chosen_brane == "eus" || chosen_brane == "mon"  || chosen_brane == "gor";
}
fn blockable_branes() -> bool {
    return chosen_brane == "mon" || chosen_brane == "gor" || chosen_brane == "lev";
}

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

use std::collections::HashMap;
use std::hash::{BuildHasherDefault, DefaultHasher};
const brane_dicts : HashMap<&str, [u16; 36]> = HashMap::from([
    ("add",
    [
        white_value, void_value, void_value, exit_value, void_value, white_value,
        void_value, void_value, void_value, white_value, white_value, void_value,
        void_value, white_value, white_value, white_value, white_value, white_value,
        white_value, white_value, player_down_solid, white_value, white_value, void_value,
        void_value, white_value, white_value, void_value, void_value, void_value,
        white_value, void_value, void_value, void_value, void_value, white_value,
    ]),
    
    ("eus",
    [
        glass_value, glass_value, glass_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, player_down_solid, white_value, glass_value, glass_value,
        glass_value, glass_value, white_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, glass_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, void_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, exit_value, glass_value, wall_value,
    ]),
    
    ("bee",
    [
        void_value, void_value, white_value, white_value, white_value, void_value,
        void_value, white_value, white_value, void_value, white_value, white_value,
        void_value, white_value, void_value, void_value, void_value, white_value,
        void_value, create_tile_data(beaver_still_entity_type, 1, exit_value), void_value, player_down_solid, white_value, void_value,
        white_value, void_value, void_value, void_value, white_value, white_value,
        wall_value, white_value, white_value, white_value, white_value, void_value,
    ]),
    
    ("mon",
    [
        rockless_button, white_value, white_value, white_value, white_value, wall_value,
        white_value, glass_value, glass_value, glass_value, glass_value, white_value,
        white_value, glass_value, white_value, glass_value, glass_value, white_value,
        white_value, glass_value, glass_value, player_down_solid, glass_value, white_value,
        white_value, glass_value, glass_value, glass_value, rock_on_glass, white_value,
        wall_value, white_value, white_value, white_value, white_value, exit_value,
    ]),
    
    ("tan",
    [
        monster_statue_on_land, hand_on_glass, player_down_solid, white_value, hand_on_glass, monster_statue_on_land,
        hand_on_glass, hand_on_glass, white_value, white_value, hand_on_glass, hand_on_glass,
        monster_statue_on_land, hand_on_glass, monster_statue_on_land, monster_statue_on_land, hand_on_glass, monster_statue_on_land,
        white_value, white_value, exit_value, hand_on_glass, white_value, white_value,
        white_value, hand_on_glass, monster_statue_on_land, white_value, hand_on_glass, white_value,
        white_value, white_value, hand_on_glass, hand_on_glass, white_value, white_value,
    ]),
    
    ("gor",
    [
        mimic_down_glass, glass_value, white_value, white_value, glass_value, player_down_glass,
        glass_value, glass_value, white_value, white_value, glass_value, glass_value,
        glass_value, glass_value, glass_value, glass_value, glass_value, white_value,
        white_value, glass_value, glass_value, glass_value, glass_value, rock_on_land,
        glass_value, glass_value, white_value, white_value, glass_value, glass_value,
        wall_value, glass_value, white_value, white_value, glass_value, exit_value,
    ]),
    
    ("lev",
    [
        wall_value, chain_inactive_value, chain_inactive_value, exit_value, white_value, player_down_solid,
        chain_inactive_value, chain_inactive_value, white_value, white_value, white_value, white_value,
        white_value, chain_inactive_value, chain_inactive_value, watcher_on_land, chain_inactive_value, chain_inactive_value,
        chain_inactive_value, chain_inactive_value, white_value, white_value, chain_inactive_value, chain_inactive_value,
        chain_inactive_value, chain_inactive_value, chain_inactive_value, chain_inactive_value, chain_inactive_value, white_value,
        watcher_on_land, white_value, chain_inactive_value, chain_inactive_value, white_value, white_value
    ]),
    
    ("cif",
    
    [
        wall_value, white_value, void_value, void_value, void_value, wall_value,
        void_value, white_value, void_value, white_value, void_value, white_value,
        void_value, white_value, void_value, void_value, white_value, void_value,
        white_value, void_value, white_value, void_value, void_value, void_value,
        white_value, void_value, void_value, player_down_solid, void_value, void_value,
        wall_value, white_value, void_value, void_value, void_value, wall_value,
    ])
]);

const brand_dicts : HashMap<&str, [bool; 36]> = HashMap::from([
    ("add",
    [
        true, false, false, false, false, true,
        false, false, false, true, true, false,
        false, true, true, true, true, true,
        true, true, true, true, true, false,
        false, true, true, false, false, false,
        true, false, false, false, false, true,
    ]),
    
    ("eus",
    [
        true, true, false, false, true, true,
        false, false, true, true, false, false,
        true, true, false, false, false, true,
        true, true, true, false, true, true,
        true, true, false, true, true, true,
        true, true, false, false, true, true,
    ]),
    
    ("bee",
    [
        false, false, false, false, false, true,
        false, false, true, true, false, false,
        true, true, true, false, false, true,
        true, false, false, true, true, true,
        true, true, false, false, true, true,
        true, true, true, false, false, true,
    ]),
    
    ("mon",
    [
        true, false, false, false, true, true,
        false, true, true, true, false, true,
        true, true, false, false, true, true,
        false, true, true, true, false, true,
        true, false, false, false, true, true,
        true, true, true, false, false, false,
    ]),
    
    ("tan",
    [
        true, false, true, true, false, true,
        false, false, true, true, false, false,
        true, false, true, true, false, true,
        true, true, false, false, true, true,
        true, false, true, true, false, true,
        true, true, false, false, true, true,
    ]),
    
    ("gor",
    [
        false, false, true, true, false, false,
        false, false, true, true, false, false,
        true, false, false, true, false, false,
        true, true, false, false, false, true,
        true, true, true, true, false, false,
        true, true, true, true, false, false,
    ]),
    
    ("lev",
    [
        true, false, false, false, true, true,
        false, false, true, true, true, true,
        true, false, false, true, false, false,
        false, false, true, true, false, false,
        false, false, false, false, false, true,
        true, true, false, false, true, true,
    ]),
    
    ("cif",
    [
        true, true, false, false, false, true,
        false, true, false, true, false, true,
        false, true, false, false, true, false,
        true, false, true, false, false, false,
        true, false, false, true, false, false,
        true, true, false, false, false, true,
    ]),
    
    ("dis",
    [
        false, false, false, false, false, false,
        false, false, false, false, false, false,
        false, false, false, false, false, false,
        false, false, false, false, false, false,
        false, false, false, false, false, false,
        false, false, false, false, false, false,
    ]),
    
    ("trailer",
    [
        true, false, false, false, false, true,
        false, false, false, false, false, false,
        false, true, false, false, true, false,
        true, true, false, false, true, true,
        false, false, false, false, false, false,
        true, false, true, true, false, true,
    ]),
    
    ("developer",
    [
        true, true, false, false, false, true,
        true, false, true, false, false, true,
        true, false, false, true, true, false,
        false, true, true, false, false, true,
        true, false, false, true, false, true,
        true, false, false, false, true, true,
    ]),
]);

const known_solutions_burdenless : HashMap<&str, &str> = HashMap::from([
    ("add+add", "URUZ"),
    
    ("eus+eus", "LRURDRZLLZLZRRZRDLZDZDZLDR"),
    ("eus+lev", "LZURRDLZLRZDDUUDZDDZURUZLDUZDZDLZRZULZRUZDZULRZRRZLLRZRLZUDZDRZLUZDDZRU"),
    ("eus+cif", "LZRRLZDLZRRLZUUDZRUDZDZUZRLZDZRZLZDUZDZDZRRUZLLUDZUZUZDDLRZUUDZUZURLDDUZDZDUZDZDLZRUUZDDUZDZDLRZUUZDZURLZLLRZURZRZ"),
    
    ("mon+eus", "UUZLDDUZUZLRZRRZLLDZDDDRRZLUULUURLZLZDLDDRDRRRZLZRRUUULZLZDZDZUUULLUDZRRDZULLDLRZRZLDZLURZUDZDUZ"),
    
    ("tan+tan", "RDDDDLUZDZULDZRUZDLUZDZRDDDLLULRZLUZUURRLZDLLUDRZRRRRLZULRZRRLZRRRUDDLLUZUUURLZDUZUDZULLUDRULZDRZUZLZ"),
    
    ("lev+lev", "LZRDDLDRDLLDLULLURURUULDLDU"),
]);

const known_solutions_wings : HashMap<&str, &str> = HashMap::from([
    ("eus+add", "DLLDDRDRZRRURULUULLDLZRURRLZLRZRZDZUZUDZLLDLZRURRZLLRZLDLZLDUZUDZRRLZRURZLZDLDZURURZLZDLUZDZRUZLUDZRRLZRZUDRZ"),
    ("eus+bee", "ULLDRZRRDDZDZDRLULULRUUZRRZLDZDZLUZRZUDZURULZL"),
    ("eus+tan", "LLRZUDDRDDLRZDURZRLZULUURZRLZRZUDDLDDUZDZ"),
]);

// Your oooother functions //

fn display_brane(brane: [u16; 36]) -> String {
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

        string.push(char_to_add);
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
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state))
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
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state))
        }
        
        // Now, check in earnest.
        let i_brane_state_land = get_land_value_from_tile(brane_state[i]);
        if i_brane_state_land == void_value && brand[i] == false {
            continue;
        }
        else if i_brane_state_land == glass_value && get_player_value_from_tile(brane_state[i]) != 0 && brand[i] == false {
            continue;
        }
        else if i_brane_state_land != void_value && i_brane_state_land != exit_value && brand[i] == true {
            continue;
        }
        return false;
    }

    return true;
}
    
// Given a brane state && a brand, returns true if the brand would be successfully carved if the tile the player is currently standing on is glass && was removed.
fn is_brand_carved_minus_stood_glass(brane_state: [u16; 36], brand: [bool; 36]) -> bool {
    for i in 0..36 {
        // First, validate the inputs to avoid any dumb mistakes.
        if brane_state[i] > max_tile_value {
            panic!("{} {}", "Error! Invalid brane_state input in is_brand_carved()!\n", display_brane(brane_state))
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
fn get_player_index(brane_state: [u16; 36], handling_absent_case: bool) -> usize {
    let mut store = 37;
    for i in 0..36 {
        if get_entity_type_from_tile(brane_state[i]) == player_entity_type {
            if store != 37 {
                panic!("Error! Multiple players found by get_player_index()\n{}",display_brane(brane_state))
            }
            store = i;
        }            
    }

    if store != 37 || handling_absent_case {
        return store;
    }

    panic!("Error! Player could not be found by get_player_index()!\n{}",display_brane(brane_state))
}

// Given a brane state, returns the index of the stairs.
fn get_stairs_index(brane_state: [u16; 36]) -> usize {
    let mut store = 37;
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == exit_value {
            if store != 37 {
                panic!("Error! Multiple stairs found by get_stairs_index()!\n{}",display_brane(brane_state))
            }
            store = i
        }
    }

    if store != 37 {
        return store
    }

    panic!("Error! Stairs could not be found by get_stairs_index()!\n{}",display_brane(brane_state))
}

// Given a brane state, returns the land value of the tile the player is standing on.
fn get_player_land_value(brane_state: [u16; 36]) -> u16 {
    return get_land_value_from_tile(brane_state[get_player_index(brane_state, false)])
}

// Given a brane state, returns the player's facing value.
fn get_player_direction_number(brane_state: [u16; 36]) -> u16 {
    return get_player_value_from_tile(brane_state[get_player_index(brane_state, false)])
}

// Given a brane state, returns the player's facing value as a letter.
fn player_faced_direction_letter(brane_state: [u16; 36]) -> char {
    return direction_number_to_letter(get_player_direction_number(brane_state) - 1);
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
        panic!("Error! No valid number equivalent for letter input in direction_letter_to_number()! {}",letter);
    }        
}

// Given a facing direction, returns the equivalent letter.
fn direction_number_to_letter(letter : u16) -> char {
    if letter == 1 {
        return 'D'
    }
    else if letter == 2 {
        return 'L'
    }
    else if letter == 3 {
        return 'U'
    }
    else if letter == 4 {
        return '4'
    }
    else {
        panic!("Error! No valid letter equivalent for number input in direction_number_to_letter()! {}",letter);
    }        
}

// Gives the tile INDEX of the tile in front of the player. Don't call this directly unless handling 37 case.
fn index_tile_in_direction_of_player(brane_state: [u16; 36], mut player_direction: char) -> usize {
    let player_i : usize = get_player_index(brane_state, false);
    if player_direction == 'X' {
        player_direction = direction_number_to_letter(get_player_value_from_tile(brane_state[player_i]));
    }

    if player_direction == 'X' {
        panic!("Error! Player does not exist to index_tile_in_front_of_player()!")
    }
    else if player_direction == 'D' { // down
        if player_i + 6 > 35 {
            return 37;
        }
        else {
            return player_i + 6;
        }
    }
    else if player_direction == 'L' { // left
        if player_i == 0 || player_i == 6 || player_i == 12 || player_i == 18 || player_i == 24 || player_i == 30 {
            return 37;
        }
        else {
            return player_i - 1;
        }
    }
    else if player_direction == 'U' { // up
        if player_i - 6 < 0 {
            return 37;
        }
        else {
            return player_i - 6;
        }
    }
    else if player_direction == 'R' { // right
        if player_i == 5 || player_i == 11 || player_i == 17 || player_i == 23 || player_i == 29 || player_i == 35 {
            return 37;
        }
        else {
            return player_i + 1;
        }
    }
    else {
        panic!("Error! Player does not have valid direction to index_tile_in_direction_of_player()! {:?}", brane_state)
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
//fn void_rod_can_take(held_tiles: Vec<u16>) -> bool {
//    return held_tiles.len() == 0 || endless;
//}

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
        return 37
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
const fn brane_has_breakable_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if breakables.contains(get_land_value_from_tile(brane_state[i])) {
            return true
        }
    }
    return false
}

// Returns true if the input brane state has an exit.
const fn brane_has_stairs_question(brane_state: [u16; 36]) -> bool {
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == exit_value {
            return true
        }
    }
    return false
}

// Counts brand-valid tiles.
const fn count_valids_in_brane(brane_state: [u16; 36]) -> u16 {
    let mut counter : u16 = 0;
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) != void_value && get_land_value_from_tile(brane_state[i]) != exit_value {
            counter += 1
        }
    }
    return counter
}

// Counts brand-valid tiles.
const fn count_valids_in_brand(brand: [bool; 36]) -> u16 {
    let mut counter : u16 = 0;
    for i in 0..36 {
        if brand[i] == true {
            counter += 1
        }
    }
    return counter
}

// Counts state-1 tiles.
const fn count_state_1s(brane_state: [u16; 36]) -> u16 {
    let mut counter : u16 = 0;
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == white_value {
            counter += 1
        }
    }
    return counter
}

// Checks if the stairs are active (i.e., available to exit from)
const fn stairs_exitable_question(brane_state: [u16; 36], held_tiles: Vec<u16>) -> bool {
    // Check the rod first.
    if held_tiles.contains(exit_value) {
        return false
    }

    // Check the brane.
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == button_value {
            // Button doesn't have a rock on it but does have a non-player entity on it.
            if get_entity_type_from_tile(brane_state[i]) == beaver_still_entity_type || get_entity_type_from_tile(brane_state[i]) == beaver_charge_entity_type || get_entity_type_from_tile(brane_state[i]) == mimic_entity_type {
                //pass
            }
            else {
                return false
            }
        }
    }

    return true
}

// Returns the number of valid tiles currently held by the wand.
fn held_valids(held_tiles: Vec<u16>) -> u16 {
    let mut counter : u16 = 0;
    for x in held_tiles {
        if x != 0 && x != 3 {
            counter += 1
        }
    }
    return counter
}
    
// Returns the number of valid tiles in the input list.
fn count_valids_gen(input: Vec<u16>) -> u16 {
    let mut counter : u16 = 0;
    for x in input {
        if x != 0 && x != 3 {
            counter += 1
        }
    }
    return counter;
}
    
// Returns taxicab distance between two points on the brane room, given by their index.
fn taxicadistance(a: u16, b: u16) -> u16 {
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
    
// Given an i value for a brane array && movements on the x && y axis, returns a new i index corresponding to that movement.
// Don't call correctly unless you're handling the 37 case.
fn move_cartesian(i: u16, x: i16, y: i16) -> u16 {
    let store = i + x + 6*y;
    
    if store > 35 || store < 0 || trunc(i/6) != trunc((i+x)/6) {
        return 37;
    }
    else {
        return u16(store);
    }
}
    
// Given a starting position && cartesian movements, returns the full tile value of the tile at that index. Accounts for OOB searching.
fn tile_at_moved_cartesian(i: u16, brane_state: [u16; 36], x: i16, y: i16) -> u16 {
    let store = move_cartesian(i, x, y);
    
    if store == 37 {
        return wall_value;
    }
    else {
        return brane_state[store];
    }
}
    
// Given a starting position && cartesian movements, returns the land value of the tile at that index. Accounts for OOB searching.
fn land_at_moved_cartesian(i: u16, brane_state: [u16; 36], x: i16, y: i16) -> u16 {
    let store = move_cartesian(i, x, y);
    
    if store == 37 {
        return wall_value;
    }
    else {
        return get_land_value_from_tile(brane_state[store]);
    }
}
    
// Returns true if the land value of this tile is 1 || (3, inactive).
fn effective_type_1(i: u16, brane_state: [u16; 36], held_tiles: Vec<u16>) -> bool {
    return (get_land_value_from_tile(i) == white_value || (get_land_value_from_tile(i) == exit_value && !stairs_exitable_question(brane_state, held_tiles))) && get_entity_type_from_tile(i) == 0
}
    
// Returns true if there is a 3 line of moveable land tiles. This includes only type-1 && inactive type-3.
fn three_line_present_strict(brane_state: [u16; 36]) -> bool {
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
fn trigger_chain_disperse(mut brane_state: [u16; 36], i: u16) -> [u16; 36] {
    if i < 0 {
        return brane_state;
    }
    
    let mut triggered_tiles : Vec<u16> = vec![i];
    
    let mut done_something = true;
    while done_something {
        done_something = false;
        
        for triggered_i in triggered_tiles {
            // Confirm land.
            if get_land_value_from_tile(brane_state[triggered_i]) != chain_active_value {
                panic!("triggered_i isn't an active chain: {} {}",triggered_i,triggered_tiles)
            }
                
            // Check each direction.
            if triggered_i-1 >= 0 && !triggered_tiles.contains(triggered_i-1) && get_land_value_from_tile(brane_state[triggered_i-1]) == chain_active_value {
                done_something = true;
                triggered_tiles.add(triggered_i-1);
                break;
            }
            if triggered_i+1 <= 35 && !triggered_tiles.contains(triggered_i+1) && get_land_value_from_tile(brane_state[triggered_i+1]) == chain_active_value {
                done_something = true;
                triggered_tiles.add(triggered_i+1);
                break;
            }
            if triggered_i-6 >= 0 && !triggered_tiles.contains(triggered_i-6) && get_land_value_from_tile(brane_state[triggered_i-6]) == chain_active_value {
                done_something = true;
                triggered_tiles.add(triggered_i-6);
                break;
            }
            if triggered_i+6 <= 35 && !triggered_tiles.contains(triggered_i+6) && get_land_value_from_tile(brane_state[triggered_i+6]) == chain_active_value {
                done_something = true;
                triggered_tiles.add(triggered_i+6);
                break;
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
    return brane_state;
}
    
// Shorthand for a use case of the above.
//fn trigger_chain_disperse_direction(brane_state: [u16; 36], direction) -> [u16; 36] {
//    return trigger_chain_disperse(brane_state,index_tile_in_direction_of_player(brane_state,direction))
//}

// Given a brane state removes any monster statues if there are no monsters present.
fn eliminate_monster_statues(mut brane_state: [u16; 36]) -> [u16; 36] {
    if here_be_monsters_question(brane_state) {
        for i in 0..36 {
            if get_rock_value_from_tile(brane_state[i]) == monster_statue_value {
                brane_state[i] = create_tile_data(0, 0, get_land_value_from_tile(brane_state[i]))
            }
        }
    }
    
    return brane_state;
}

// Triggers the first untriggered watcher statue found.
fn trigger_one_watcher(mut brane_state: [u16; 36]) -> [u16; 36] {
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == watcher_statue_inactive_value {
            brane_state[i] += watcher_statue_active_value - watcher_statue_inactive_value;
            return brane_state;
        }
    }
    return brane_state;
}

// Returns true if every watcher statue is triggered. Returns false is there are none.
fn all_watchers_triggered(brane_state: [u16; 36]) -> bool {
    let mut any_present = false;
    for i in 0..36 {
        if get_land_value_from_tile(brane_state[i]) == watcher_statue_inactive_value {
            return false;
        }
        else if get_land_value_from_tile(brane_state[i]) == watcher_statue_active_value {
            any_present = true;
        }
    }
            
    return any_present;
}

fn burdenless() -> bool {
    return !wings && !sword && !endless
}
fn only_wings() -> bool {
    return wings && !sword && !endless
}
fn only_sword() -> bool {
    return !wings && sword && !endless
}

// Returns true if for the given state, there is ABSOLUTELY no way to recover. In this case we do not even check the node || its descendants. This has the potential to shave exponential amounts of nodes, so the more scenarios this can detect, the better.
fn unrecoverable_branch(game_state: ([u16; 36], Vec<u16>)) -> bool {
    // Less tiles than needed.
    let doomed_glass_factor = (any_glass && standing_on_glass(game_state[0])) as u16;
    if count_valids_in_brane(game_state[0]) + count_valids_gen(game_state[1]) - doomed_glass_factor < valids_in_brand {
        return true
    }
        
    // Block where there shouldn't be. Only check in situations where it's possible to softlock.
    if blockable_branes {
        for i in [0,5,30,35] {
            if game_state[0][i] == wall_value && brand_dicts.get(chosen_brand)[i] == void_value {
                return true
            }
        }
    }
        
    // Default
    return false
}

// Pickle stuff
fn pickle_name_sub() {
    if sword {
        if wings {
            if endless {
                return "winged_sword_endless"
            }
            else {
                return "winged_sword_finite"
            }
        }
        else {
            if endless {
                return "wingless_sword_endless"
            }
            else {
                return "wingless_sword_finite"
            }
        }
    }
    else {
        if wings {
            if endless {
                return "winged_swordless_endless"
            }
            else {
                return "winged_swordless_finite"
            }
        }
        else {
            if endless {
                return "wingless_swordless_endless"
            }
            else {
                return "wingless_swordless_finite"
            }
        }
    }
}

fn gs_pickle_name() {
    return "movement_dicts/"+pickle_name_sub()+"/"+combo_name()+"/game_state.pkl"
}
fn vn_pickle_name() {
    return "movement_dicts/"+pickle_name_sub()+"/"+combo_name()+"/visited_nodes.pkl"
}
fn nntc_pickle_name() {
    return "movement_dicts/"+pickle_name_sub()+"/"+combo_name()+"/next_nodes_to_check.pkl"
}
fn pfst_pickle_name() {
    return "movement_dicts/"+pickle_name_sub()+"/"+combo_name()+"/path_from_source_to.pkl"
}
fn bfs_pickle_name() {
    return "movement_dicts/"+pickle_name_sub()+"/"+combo_name()+"/search_counter.pkl"
}

fn main() {
    // State traversal function has a special spot right here. //
    const special_error : ([u16; 36], Vec<u16>) = ([37,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], vec![]);
    fn brane_walk(mut game_state: ([u16; 32], Vec<u16>), input: char) -> ([u16; 32], Vec<u16>) {
        // Validation.
        if !endless && game_state[1].len() > 1 {
            panic!("brane_walk passed multi-tile held without endless.")
        }
        
        // Get player index
        let player_index = get_player_index(game_state[0], true);
        if player_index == 37 {
            return special_error;
        }
        let player_land_data = get_land_value_from_tile(game_state[0][player_index]);
        
        // Beaver sees player. (haven't coded excluding vision through walls, no need to)
        if chosen_brane == "bee" {
            for i in 0..36 {
                // Found inactive beaver.
                if get_entity_type_from_tile(game_state[0][i]) == beaver_still_entity_type {
                    // Beaver is in LoS of player.
                    if collumn_values(game_state[0], get_collumn(i)).contains(player_entity_type) || row_values(game_state[0], row_collumn(i)).contains(player_entity_type) {
                        // Set beaver facing && in charge state; makes actual movement after player.
                        if i - player_index >= 6 { // charge up.
                            game_state[0][i] = create_tile_data(beaver_charge_entity_type, 3, get_land_value_from_tile(game_state[0][i]));
                        }
                        else if player_index - i >= 6 { // charge down.
                            game_state[0][i] = create_tile_data(beaver_charge_entity_type, 1, get_land_value_from_tile(game_state[0][i]));
                        }
                        else if player_index > i { // charge right
                            game_state[0][i] = create_tile_data(beaver_charge_entity_type, 4, get_land_value_from_tile(game_state[0][i]));
                        }
                        else if player_index < i { // charge left
                            game_state[0][i] = create_tile_data(beaver_charge_entity_type, 2, get_land_value_from_tile(game_state[0][i]));
                        }
                    }
                        
                    // There is only one beaver. In case of scope creep, disable.
                    break;
                }
            }
        }
        // Player action.
        if input == 'Z' {
            let full_faced_tile_data = tile_in_direction_of_player(game_state[0], 'X');
            let faced_land_data = get_land_value_from_tile(full_faced_tile_data);
            
            // Slaaaaaayy the beaaast!!!
            if sword && ([beaver_still_entity_type, beaver_charge_entity_type, mimic_entity_type].contains(get_entity_type_from_tile(full_faced_tile_data)) || get_rock_value_from_tile(full_faced_tile_data) == hands_present_value) {
                game_state[0][index_tile_in_direction_of_player(game_state[0], 'X')] = create_tile_data(0,0,faced_land_data);
                game_state[0] = eliminate_monster_statues(game_state[0]);
            }       
            // Is tile invalid for both pickup && placedown?
            else if full_faced_tile_data != faced_land_data || faced_land_data == wall_value { // (Explanation: this inequality means there is an entity on the tile, meaning an enemy || a rock. The second one is just checking if the tile is a wall, which is self-explanatory.) 
                return special_error;
            }
            // Tile is valid for pickup.
            else if faced_land_data != void_value && faced_land_data != wall_value && void_rod_can_take(game_state[1]) {
                // Put tile on void rod.
                game_state[1].append(faced_land_data);
    
                // Remove the tile from the world.
                game_state[0][index_tile_in_direction_of_player(game_state[0], 'X')] = 0;
                
                // Bump watcher statues.
                if chosen_brane == "lev" {
                    game_state[0] = trigger_one_watcher(game_state[0]);
                    if all_watchers_triggered(game_state[0]) {
                        game_state[0][player_index] = create_tile_data(0,0,player_land_data);
                        return game_state;
                    }
                }
            }
            // Placing tile.
            else if full_faced_tile_data == void_value && game_state[1].len() > 0 {
                // Place the tile into the world.
                game_state[0][index_tile_in_direction_of_player(game_state[0], 'X')] = game_state[1][-1];
    
                // Remove the tile from the void rod.
                game_state[1].pop();
                
                // Bump watcher statues.
                if chosen_brane == "lev" {
                    game_state[0] = trigger_one_watcher(game_state[0]);
                    if all_watchers_triggered(game_state[0]) {
                        game_state[0][player_index] = create_tile_data(0,0,player_land_data);
                        return game_state;
                    }
                }
            }
            // Cannot do anything.
            else {
                return special_error;
            }
        }
        else if input == 'D' || input == 'L' || input == 'U' || input == 'R' {
            let moving_tile_index = index_tile_in_direction_of_player(game_state[0], input);
    
            let mut full_moving_tile_data : u16 = 0;
            let mut moving_land_data : u16 = 0;
    
            if moving_tile_index == 37 {
                full_moving_tile_data = wall_value;
                moving_land_data = wall_value;
            }
            else {
                full_moving_tile_data = tile_in_direction_of_player(game_state[0], input);
                moving_land_data = get_land_value_from_tile(full_moving_tile_data);
            }
    
            // Moving into a hand (hands!)
            if get_rock_value_from_tile(full_moving_tile_data) == hands_present_value {
                return special_error
            }
            // Moving into a rock || statue.
            else if get_rock_value_from_tile(full_moving_tile_data) != 0 {
                // Determine tile the rock is moving into.
                let mut rock_destination_index = -1;
                let mut rock_destination_tile_value = 0;
                if input == 'D' {
                    rock_destination_index = move_cartesian(player_index,0,2);
                    rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],0,2);
                }
                else if input == 'L' {
                    rock_destination_index = move_cartesian(player_index,-2,0);
                    rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],-2,0);
                }
                else if input == 'U' {
                    rock_destination_index = move_cartesian(player_index,0,-2);
                    rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],0,-2);
                }
                else if input == 'R' {
                    rock_destination_index = move_cartesian(player_index,2,0);
                    rock_destination_tile_value = tile_at_moved_cartesian(player_index,game_state[0],2,0);
                }
                else {
                    panic!("Unrecognized input: {}",input)
                }
                
                let rock_destination_land_value = get_land_value_from_tile(rock_destination_tile_value);
                let rock_destination_rock_value = get_rock_value_from_tile(rock_destination_tile_value);
                
                // Player does a push.
                if floating(game_state[0]) {
                    game_state[0][player_index] = void_value;
                }
                else {
                    game_state[0][player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data);
                }
                
                // If this is a wall || another rock, it can't move.
                if rock_destination_land_value == wall_value || (rock_destination_rock_value != 0 && rock_destination_rock_value != hands_present_value) {
                    //pass
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
                        //pass
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
                        game_state[0] = trigger_chain_disperse(game_state[0], rock_destination_index);
                        game_state[0] = eliminate_monster_statues(game_state[0]);
                            
                        return game_state
                    }
                    // Unhandled tile type.
                    else {
                        panic!("Error! Cannot resolve world state!1 {} {} ",input,rock_destination_land_value);
                    }
                        
                    // Destroy monster statues if need be.
                    game_state[0] = eliminate_monster_statues(game_state[0]);
                        
                    // Corner true-rocks are walls.
                    if (rock_destination_index == 0 || rock_destination_index == 5 || rock_destination_index == 30 || rock_destination_index == 35) && get_rock_value_from_tile(full_moving_tile_data) == rock_present_value && get_land_value_from_tile(game_state[0][rock_destination_index]) != chain_active_value {
                        game_state[0][rock_destination_index] = wall_value;
                    }
                }
            }
            else {
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
                        game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), 0);
                    }
                }
                // Tile is a solid tile, glass, chain, button, || walkable stairs.
                else if moving_land_data == white_value || moving_land_data == glass_value || moving_land_data == chain_inactive_value || moving_land_data == button_value || (moving_land_data == exit_value && !stairs_exitable_question(game_state[0],game_state[1])) {
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
                            panic!("6moving_tile_index == -1 && was attempted to be used as an index");
                        }
                        game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), chain_active_value)
                    }
                    else {
                        if moving_tile_index == -1 {
                            panic!("7moving_tile_index == -1 && was attempted to be used as an index");
                        }
                        game_state[0][moving_tile_index] = create_tile_data(1, direction_letter_to_number(input), moving_land_data)
                    }
                }
                // Tile we're moving into is active stairs.
                else if moving_land_data == exit_value && stairs_exitable_question(game_state[0],game_state[1]) {
                    return special_error
                }
                // Tile is a wall. This is basically the same as solid tile except we only change the facing direction.
                else if moving_land_data == wall_value {
                    if floating(game_state[0]) {
                        game_state[0][player_index] = void_value;
                        return game_state;
                    }
                    else {
                        game_state[0][player_index] = create_tile_data(1, direction_letter_to_number(input), player_land_data);
                        
                        // Simply changing your direction to face directly into a wall is never useful unless you're wasting a turn. If there are no moving monsters, wasting turns is pointless. Therefore we can eleminate these from the state space graph.
                        if chosen_brane == "add" || chosen_brane == "eus" || chosen_brane == "mon" || chosen_brane == "tan" || chosen_brane == "lev" || chosen_brane == "cif" || !here_be_moving_monsters_question(game_state[0]) {
                            return special_error;
                        }
                    }
                }
                else {
                    panic!("Error! Cannot resolve world state!2 {} {}",input,moving_land_data);
                }
            }            
        }
        else {
            panic!("Error! Cannot resolve world state!3 {}",input)
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
          
        return game_state;
    }
    
    // Test BS.
    //println!("{}", display_brane(add_brane, false));
    //println!("There is nothing.");
    
    // Begin!
    println!("WINGS: {}",wings);
    println!("SWORD: {}",sword);
    println!("ENDLESS: {}",endless);
    
    chosen_brane = input("Starting brane? (You may also type wings, sword, || endless to toggle them.)\n");
    chosen_brane = chosen_brane.lower();
    
    if chosen_brane == "wings" {
        wings = !wings;
        continue;
    }
    else if chosen_brane == "sword" {
        sword = !sword;
        continue;
    }
    else if chosen_brane == "endless" {
        endless = !endless;
        continue;
    }
        
    chosen_brand = input("...And the brand?\n");
    chosen_brand = chosen_brand.lower();
    
    if chosen_brand == "dev" {
        chosen_brand = "developer";
    }
    
    if !brane_dicts.contains(chosen_brane) || !brand_dicts.contains(chosen_brand) {
        print!("Invalid inputs. Try again.");
        continue;
    }
    else if count_valids_in_brane(brand_dicts.get(chosen_brand)) > count_valids_in_brane(brane_dicts.get(chosen_brane)) {
        print!("Target brand has more tiles than the selected brane does. This will never work!");
        continue;
    }
    else if !endless && count_valids_in_brane(brand_dicts.get(chosen_brand)) < count_state_1s(brane_dicts.get(chosen_brane)) {
        print!("Target brand has less tiles than the selected brane does, we do not have the endless void rod, && there are not enough glass tiles to compensate. This will never work!");
        continue;
    }
    else if chosen_brand == "dis" && !brane_has_breakable_question(brane_dicts.get(chosen_brane)) {
        print!("Attempting to carve the DIS brand, but the selected brane has no glass, meaning the best we could ever do is 1 lone tile. This will never work!");
        continue;
    }
        
    if sword && !here_be_monsters_question(brane_dicts.get(chosen_brane)) {
        print!("Sword is enabled but there are no monsters. Disabling for irrelevancy.")
    }
    
    let mut flag = false;
    for i in 0..36 {
        if brane_dicts.get(chosen_brane)[i] == wall_value && brand_dicts.get(chosen_brand)[i] == void_value {
            flag = true;
            break;
        }
    }
    
    if flag {
        print!("Target brand has an empty space where the brane has a wall. This will never work!");
        continue;
    }
    
    // Resets this as irrelevant.
    //if predestination_mode && !(burdenless() && combo_name() in known_solutions_burdenless) && !(only_wings() && combo_name() in known_solutions_wings) {
    //    print!("Brane/brand combination not in solution list, disabling predestination mode.");
    //    predestination_mode = false;
    //}
    
    // Create pickling path
    use std::fs;
    fs::create_dir_all("movement_dicts/"+pickle_name_sub()+"/")?;
     
    // Begin breadth-first search.
    // Specific functions.
        
    //import json;
    //fn hashable_game_state(game_state: tuple[list]) -> String {
    //    return json.dumps(game_state);
    //}
        
    // Given a hashabled node, returns the brane state only.
    //fn brane_state_from_hasabled_node(node: String) -> [u16; 36] {
    //    return json.loads(node)[0];
    //}
        
    // Given a hashabled node, returns the whole game state.
    //fn unhashablize_node(node: String) -> ([u16; 36], Vec<u16>) {
    //    return json.loads(node);
    //}
        
    // Returns true if the player is standing on glass.
    fn standing_on_glass(brane_state: [u16; 36]) -> bool {
        return get_land_value_from_tile(brane_state[get_player_index(brane_state, false)]) == glass_value;
    }
    
    // Attempt to load our pickled dictionary.
    use serde::{Serialize, Deserialize};
    let mut movement_state_dictionary : HashMap<([u16; 36], Vec<u16>), [([u16; 36], Vec<u16>); 5]> = serde_json::from_str(fs::read_to_string(gs_pickle_name()).expect("Should have been able to read the file")).unwrap();
    
    // A node is defined as a "game state", a tuple containing first the brane state, then the held tiles. Together, these uniquely define a game position. (The changed applied by the wings, sword, && void rod are situational && handled separately.)
    
    // Keep a set of all visited nodes. If we ever re-visit them, we ignore it.
    let mut visited_nodes : Vec<([u16; 36], Vec<u16>)> = serde_json::from_str(fs::read_to_string(vn_pickle_name()).expect("Should have been able to read the file")).unwrap();
    let len_visited_nodes_cache = visited_nodes.len();
    
    // Dictionary of paths.
    let mut path_from_source_to : HashMap<([u16; 36], Vec<u16>), String> = serde_json::from_str(fs::read_to_string(pfst_pickle_name()).expect("Should have been able to read the file")).unwrap();
    path_from_source_to.insert((brane_dicts.get(chosen_brane), vec![]), "");
        
    // Begin our search at the very beginning, holding nothing.
    let mut nodes_to_check : Vec<([u16; 36], Vec<u16>)> = vec![];
    let mut next_nodes_to_check : ([u16; 36], Vec<u16>) = serde_json::from_str(fs::read_to_string(nntc_pickle_name()).expect("Should have been able to read the file")).unwrap();
    next_nodes_to_check.insert((brane_dicts.get(chosen_brane), vec![]));
    
    // Timestamp
    use std::time::{Instant};
    let dfs_timestamp = Instant::now();
    
    // Movement-dictionary saving counter
    let mut md_counter = 0;
    
    // BFS counter
    let mut bfs = -1;
    bfs = serde_json::from_str(fs::read_to_string(bfs_pickle_name()).expect("Should have been able to read the file")).unwrap();
    
    print!("Beginning breadth-first search.");
    while next_nodes_to_check.len() > 0 {
        bfs += 1;
        print!("BFS iteration {}",bfs);
        use std::fs::File;
        write!(File::create(bfs_pickled_name())?, "{}", serde_json::to_string(bfs).unwrap());
        
        // Even if we're not burdenless, going longer than the burdenless solution can only mean we're doing something wrong.
        if known_solutions_burdenless.contains(combo_name()) && bfs > known_solutions_burdenless[combo_name()].len() {
            panic!("BFS exceeds known burdenless solution length. Something went very wrong. Deleting cache is recommended.");
        }
        else if only_wings() && known_solutions_wings.contains(combo_name()) && bfs > known_solutions_wings[combo_name()].len() {
            panic!("BFS exceeds known winged solution length. Something went very wrong. Deleting cache is recommended.");
        }
        
        // Pickle cache.
        write!(File::create(gs_pickled_name())?, "{}", serde_json::to_string(movement_state_dictionary).unwrap());
            
        // Create the checklist for upcoming loop.
        nodes_to_check = next_nodes_to_check - visited_nodes;
        next_nodes_to_check.clear();
        
        // Stash in case of crash.
        write!(File::create(vn_pickled_name())?, "{}", serde_json::to_string(visited_nodes).unwrap());
        write!(File::create(nntc_pickled_name())?, "{}", serde_json::to_string(next_nodes_to_check).unwrap());
        write!(File::create(pfst_pickled_name())?, "{}", serde_json::to_string(path_from_source_to).unwrap());

        let mut counter = -1;
        // Iterate through each node.
        for node in nodes_to_check {
            // Debug
            counter += 1;
            //print!(display_brane(brane_state_from_hasabled_node(node)))
            println!("Layer {}",bfs);
            println!("{} / {}",counter,nodes_to_check.len());
            
            //while true {
            //    print!(node)
            
            // Check if we've been here before. If so, no need to recalculate.
            //if node in visited_nodes {
            //    print!("Notice! This is a backup measure that shouldn't be getting triggered.")
            //    continue
            
            // Easier check to do, if possible.
            if !endless && node[1].len() == 0 {
                //pass
            }
            // Check to see if this node is solved.
            else if is_brand_carved(node[0], brand_dicts.get(chosen_brand)) {
                // Report it.
                let time_at_success = Instant::now();
                loop {
                    print!("{}", display_brane(node[0]));
                    print!("WE DID IT WE DID IT");
                    print!("{}",combo_name_full());
                    print!("Took {} seconds to visit {} nodes.",time_at_success - dfs_timestamp,visited_nodes.len()-len_visited_nodes_cache);
                    print!("Average time-per-node: {}",(time_at_success - dfs_timestamp)/(visited_nodes.len()-len_visited_nodes_cache));
                    print!("{}", path_from_source_to[node]);
                    
                    use std::io::{stdin,stdout,Write};
                    let mut s=String::new();
                    print!("Please enter some text: ");
                    let _=stdout().flush();
                    stdin().read_line(&mut s).expect("Did not enter a correct string");
                }
            }
            
            // Establish cache value if needed.
            if !movement_state_dictionary.contains(node) {
                movement_state_dictionary.insert(
                    node,
                    
                    [
                        hashable_game_state(brane_walk(node, "D", true)),
                        hashable_game_state(brane_walk(node, "L", true)),
                        hashable_game_state(brane_walk(node, "U", true)),
                        hashable_game_state(brane_walk(node, "R", true)),
                        hashable_game_state(brane_walk(node, "Z", true)),
                    ],
                );
                
                // Save our cache every so often.
                md_counter += 1;
                if md_counter % 10000 == 0 {
                    write!(File::create(gs_pickled_name())?, "{}", serde_json::to_string(movement_state_dictionary).unwrap());
                }
            }
                
            // Establish paths.
            for i in range(5) {
                if path_from_source_to.contains(movement_state_dictionary.get(node)[i]) {
                    continue
                }
                
                path_from_source_to.insert(
                    movement_state_dictionary.get(node)[i],
                    path_from_source_to.get(node) + ("D","L","U","R","Z")[i],
                );
            }
                
            // Add neighbors to set.
            for x in movement_state_dictionary.get(node) {
                if x == special_error {
                    //pass
                }
                else if unrecoverable_branch(x) {
                    //pass
                }
                else {
                    next_nodes_to_check.add(x);
                }
            }
            
            // Establish having been here.
            visited_nodes.add(node);
            
            // Periodically stash in cash of crash. Don't do this too often || else it will slow shit way down.
            if counter % 10000 == 0 {
                //pickle.dump(visited_nodes, open(vn_pickle_name(), 'wb'))
                //pickle.dump(nodes_to_check | next_nodes_to_check, open(nntc_pickle_name(), 'wb'))
                write!(File::create(pfst_pickled_name())?, "{}", serde_json::to_string(path_from_source_to).unwrap());
            }
        }
    }

    // No success found.
    loop {
        if known_solutions_burdenless.contains(combo_name()) {
            print!("Combination exists in known solutions. This is wrong.")
        }
        use std::io::{stdin,stdout,Write};
        let mut s=String::new();
        print!("\"Searched far && wide, have I. The boy's home does not exist.\"\nExhaustively searched. No solution found. Proved impossible unless something went wrong.");
        let _=stdout().flush();
        stdin().read_line(&mut s).expect("Did not enter a correct string");
    }
}