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

    // New data structure:
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

fn display_brane(brane: [u16; 36], ignoring_length: bool) -> String {
    if !ignoring_length && brane.len() != 36 {
        panic!("Error! Brane with invalid length.")
    }
    
    let mut string : String = String::from("");
    
    for i in 0..brane.len() {
        let mut string_to_add = "?";
        
        if brane[i] == void_value {
            string_to_add = "_";
        }
        else if brane[i] == white_value {
            if stupid_display_crap {
                string_to_add = "#";
            }
            else {
                string_to_add = "█";
            }
        }
        else if brane[i] == glass_value {
            string_to_add = "/";
        }
        else if brane[i] == exit_value {
            string_to_add = "S";
        }
        else if brane[i] == wall_value {
            string_to_add = "W";
        }
        else if brane[i] == chain_inactive_value {
            if stupid_display_crap {
                string_to_add = "0";
            }
            else {
                string_to_add = "Θ";
            }
        }
        else if brane[i] == chain_active_value {
            if stupid_display_crap {
                string_to_add = "*";
            }
            else {
                string_to_add = "•";
            }
        }
        else if brane[i] == button_value {
            string_to_add = "B";
        }
        
        if get_rock_value_from_tile(brane[i]) == rock_present_value {
            string_to_add = "R";
        }
        else if get_rock_value_from_tile(brane[i]) == hands_present_value {
            string_to_add = "H";
        }
        
        if get_player_value_from_tile(brane[i]) == 1 {
            string_to_add = "V";
        }
        else if get_player_value_from_tile(brane[i]) == 2 {
            string_to_add = "<";
        }
        else if get_player_value_from_tile(brane[i]) == 3 {
            string_to_add = "^";
        }
        else if get_player_value_from_tile(brane[i]) == 4 {
            string_to_add = ">";
        }

        string.push_str(string_to_add);
        string.push(' ');

        if i == 5 || i == 11 || i == 17 || i == 23 || i == 29 {
            string.push('\n');
        }
    }
    
    return string
}

fn main() {
    println!("{}", display_brane(add_brane, false));
    println!("There is nothing.");
}