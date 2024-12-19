import json
from math import ceil

DIRECTION_4_TO_OFFSET = [[0, -1], [1, 0], [0, 1], [-1, 0]]

CUSTOM_GENERIC_TERMS = new_categories = {
    "power-generation": [
        "boiler",
        "steam-engine",
        "solar-panel",
        "nuclear-reactor",
        "fusion-generator",
        "fusion-reactor",
        "steam-turbine"
    ],
    "labs": [
        "lab",
        "biolab"
    ],
    "power-distribution": [
        "big-electric-pole",
        "medium-electric-pole",
        "small-electric-pole",
        "substation",
        "power-switch"
    ],
    "robotic-logistics": [
        "roboport",
        "active-provider-chest",
        "buffer-chest",
        "passive-provider-chest",
        "requester-chest",
        "storage-chest"
    ]
}

def load_json_file(filename):
    """Load and return JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def get_subgroup_mappings(item_json):
    """Create mapping of subgroups to their parent groups."""
    subgroup_to_group = {}
    valid_groups = {"combat", "logistics", "production", "space"}
    
    for subgroup in item_json['item-subgroup'].values():
        subgroup_name = subgroup['name']
        group_name = subgroup['group']
        if group_name in valid_groups:
            subgroup_to_group[subgroup_name] = group_name
    
    return subgroup_to_group

def get_base_items(item_json, subgroup_to_group):
    """Get base items and their properties."""
    items = {}
    for item in item_json['item'].values():
        if 'subgroup' not in item:
            continue

        subgroup_name = item['subgroup']
        item_name = item['name']

        if subgroup_name in subgroup_to_group:
            items[item_name] = {
                "group": subgroup_to_group[subgroup_name],
                "subgroup": subgroup_name,
            }
    
    return items

def add_special_items(items):
    """Add special items that can't be built directly."""
    special_items = [
        "straight-rail", "half-diagonal-rail", "curved-rail-a", "curved-rail-b",
        "rail-ramp", "rail-support", "elevated-straight-rail",
        "elevated-half-diagonal-rail", "elevated-curved-rail-a", "elevated-curved-rail-b"
    ]
    
    for item in special_items:
        items[item] = {
            "group": "logistics",
            "subgroup": "train-transport",
        }
    return items

def process_pipe_connections(data, key2):
    """Process pipe connections from fluid boxes."""
    pipe_connections = []
    for key3 in data.keys():
        if key3 == "fluid_boxes":
            for fluid_box in data[key3]:
                pipe_connections.extend(fluid_box["pipe_connections"])
        elif key3.endswith("fluid_box"):
            pipe_connections.extend(data[key3]["pipe_connections"])
    
    return process_connections(pipe_connections, key2)

def process_connections(connections, item_name):
    """Process connection positions and return target positions."""
    target_positions = []
    for connection in connections:
        if item_name == "pumpjack":  # Special case handling
            connection["position"] = connection["positions"][0]
        
        offset = DIRECTION_4_TO_OFFSET[connection["direction"]//4]
        pos = connection["position"]
        target_position = [pos[0] + offset[0], pos[1] + offset[1]]
        target_positions.append([pos, target_position])
    return target_positions

def process_heat_connections(data, key2):
    """Process heat connections from energy source and heat buffer."""
    heat_connections = []
    for heat_source in ['energy_source', 'heat_buffer']:
        if (heat_source in data and isinstance(data[heat_source], dict) and 
            "connections" in data[heat_source]):
            heat_connections.extend(data[heat_source]["connections"])
    
    return process_connections(heat_connections, key2)

def get_fluid_recipes(recipe_json):
    """Get recipes that involve fluids."""
    fluid_recipes = []
    for recipe in recipe_json['recipe'].values():
        if has_fluid_component(recipe):
            fluid_recipes.append(recipe['name'])
    return fluid_recipes

def has_fluid_component(recipe):
    """Check if a recipe has fluid ingredients or results."""
    # Check ingredients
    if 'ingredients' in recipe:
        for ingredient in recipe['ingredients']:
            if isinstance(ingredient, dict) and ingredient.get('type') == 'fluid':
                return True
    
    # Check results
    if 'results' in recipe:
        for result in recipe['results']:
            if isinstance(result, dict) and result.get('type') == 'fluid':
                return True
    return False

def get_tile_layers(factorio_json):
    """Extract tile names and their layers from factorio data."""
    tiles = []
    if 'tile' in factorio_json:
        for tile_name, tile_data in factorio_json['tile'].items():
            if tile_name == "landfill":
                tiles.append((tile_name, -1))
            elif "subgroup" in tile_data and tile_data["subgroup"] == "artificial-tiles" and 'layer' in tile_data:
                tiles.append((tile_name, tile_data['layer']))
    
    # Sort by layer number ascending
    tiles.sort(key=lambda x: x[1])
    return [name for name, _ in tiles]

def generate_js_output(sorted_items, pipe_positions, heat_positions, fluid_recipes, tile_layers):
    """Generate JavaScript output strings."""
    js_output = ["// This file is generated by get_items.py\n"]
    js_output.append("const entityNameToProperties = {")
    current_group = None
    current_subgroup = None

    # Add sorted items
    for item_name, item_data in sorted_items.items():
        if item_data["group"] != current_group:
            js_output.append(f"\n    // Group: {item_data['group'].capitalize()}")
            current_group = item_data["group"]
        if item_data["subgroup"] != current_subgroup:
            js_output.append(f"    // Subgroup: {item_data['subgroup']}")
            current_subgroup = item_data["subgroup"]
        
        js_output.append(format_item_entry(item_name, item_data))
    
    js_output.append("}")

    # Add generic terms
    generic_terms = collect_generic_terms(sorted_items)
    generic_terms.update(CUSTOM_GENERIC_TERMS)
    js_output.extend([
        "\nconst buildingGenericTerms = {",
        *[f'    "{group}": {json.dumps(terms)},' for group, terms in sorted(generic_terms.items())],
        "}"
    ])

    # Add pipe target positions
    js_output.extend([
        "\nconst itemToPipeTargetPositions = {",
        *[f'    "{item}": {str(pos)},' for item, pos in sorted(pipe_positions.items())],
        "}"
    ])

    # Add heat target positions
    js_output.extend([
        "\nconst itemToHeatTargetPositions = {",
        *[f'    "{item}": {str(pos)},' for item, pos in sorted(heat_positions.items())],
        "}"
    ])

    # Add fluid recipes
    js_output.extend([
        "\nconst fluidRecipes = {",
        *[f'    "{recipe}": true,' for recipe in sorted(fluid_recipes)],
        "}"
    ])

    # Add tile layers
    js_output.extend([
        "\nconst artificialTilesSortedByLayer = [",
        *[f'    "{tile}",' for tile in tile_layers],
        "]"
    ])

    return js_output

def format_item_entry(item_name, item_data):
    """Format a single item entry for JavaScript output."""
    item_data['genericTerms'] = [item_data['group'], item_data['subgroup']]
    
    props = {
        "genericTerms": item_data['genericTerms']
    }
    if item_name not in ["curved-rail-a", "curved-rail-b", "elevated-curved-rail-a", "elevated-curved-rail-b", "elevated-half-diagonal-rail", "elevated-straight-rail", "half-diagonal-rail"]:
        props["size"] = [
            ceil(item_data['collision_box'][1][0] - item_data['collision_box'][0][0]),
            ceil(item_data['collision_box'][1][1] - item_data['collision_box'][0][1])
        ]
        props["selection_size"] = [
            item_data['selection_box'][1][0] - item_data['selection_box'][0][0],
            item_data['selection_box'][1][1] - item_data['selection_box'][0][1]
        ]
        props["collision_size"] = [
            item_data['collision_box'][1][0] - item_data['collision_box'][0][0],
            item_data['collision_box'][1][1] - item_data['collision_box'][0][1]
        ]
    
    if "pipe_connection_target_positions" in item_data:
        props["pipeConnectionTargetPositions"] = item_data['pipe_connection_target_positions']
    
    return f'    "{item_name}": {str(props)},'

def collect_generic_terms(sorted_items):
    """Collect all generic terms grouped by their group and subgroups."""
    generic_terms = {}
    
    # Initialize mappings
    for item_name, item_data in sorted_items.items():
        group = item_data['group']
        subgroup = item_data['subgroup']
        
        # Initialize group-to-items mapping
        if group not in generic_terms:
            generic_terms[group] = set()
        generic_terms[group].add(item_name)
        
        # Initialize subgroup-to-items mapping
        if subgroup not in generic_terms:
            generic_terms[subgroup] = set()
        generic_terms[subgroup].add(item_name)
    
    # Convert sets to sorted lists
    return {key: sorted(list(terms)) for key, terms in generic_terms.items()}

def main():
    # Load JSON data
    item_json = load_json_file('factorio_data/item_data.json')
    factorio_json = load_json_file('factorio_data/factorio_data.json')
    recipe_json = load_json_file('factorio_data/recipe_data.json')

    # Process data
    subgroup_to_group = get_subgroup_mappings(item_json)
    items = get_base_items(item_json, subgroup_to_group)
    items = add_special_items(items)

    # Process connections
    item_to_pipe_target_positions = {}
    item_to_heat_target_positions = {}

    for key1, data1 in factorio_json.items():
        if isinstance(data1, dict):
            for key2, data2 in data1.items():
                if key2 not in items:
                    continue
                if "collision_box" not in data2 or "selection_box" not in data2:
                    continue

                items[key2].update({
                    "collision_box": data2["collision_box"],
                    "selection_box": data2["selection_box"]
                })

                pipe_targets = process_pipe_connections(data2, key2)
                if pipe_targets:
                    item_to_pipe_target_positions[key2] = pipe_targets

                heat_targets = process_heat_connections(data2, key2)
                if heat_targets:
                    item_to_heat_target_positions[key2] = heat_targets

    # Remove items without collision box and sort
    items = {name: data for name, data in items.items() if "collision_box" in data}
    sorted_items = dict(sorted(items.items(), key=lambda x: (x[1]['group'], x[1]['subgroup'], x[0])))

    # Generate output
    fluid_recipes = get_fluid_recipes(recipe_json)
    tile_layers = get_tile_layers(factorio_json)
    js_output = generate_js_output(sorted_items, item_to_pipe_target_positions, 
                                 item_to_heat_target_positions, fluid_recipes, tile_layers)

    # Write output
    with open('entityProperties.js', 'w') as file:
        file.write('\n'.join(js_output))

if __name__ == "__main__":
    main()

