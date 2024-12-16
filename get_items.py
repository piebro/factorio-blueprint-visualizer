import json

# Read both JSON files
with open('factorio_data/item_data.json', 'r') as file:
    item_json = json.load(file)

with open('factorio_data/factorio_data.json', 'r') as file:
    factorio_json = json.load(file)

# Read recipe data
with open('factorio_data/recipe_data.json', 'r') as file:
    recipe_json = json.load(file)

items = {}
subgroup_to_group = {}

for subgroup in item_json['item-subgroup'].values():
    subgroup_name = subgroup['name']
    group_name = subgroup['group']
    if group_name in ["combat", "logistics", "production", "space"]:
        subgroup_to_group[subgroup_name] = group_name

for item in item_json['item'].values():
    if 'subgroup' not in item.keys():
        continue

    subgroup_name = item['subgroup']
    item_name = item['name']

    if subgroup_name in subgroup_to_group:
        items[item_name] = {
            "group": subgroup_to_group[subgroup_name],
            "subgroup": subgroup_name,
        }


for extra_item in ["straight-rail", "half-diagonal-rail", "curved-rail-a", "curved-rail-b", "rail-ramp", "rail-support", "elevated-straight-rail", "elevated-half-diagonal-rail", "elevated-curved-rail-a", "elevated-curved-rail-b"]:
    items[extra_item] = {
        "group": "logistics",
        "subgroup": "train-transport",
    }

DIRECTION_4_TO_OFFSET = [[0, -1], [1, 0], [0, 1], [-1, 0]];

item_to_pipe_target_positions = {}
item_to_heat_target_positions = {}

# Create a dictionary of all available items from factorio_data (all nested keys with their values)
for key1, data1 in factorio_json.items():
    if isinstance(data1, dict):
        for key2, data2 in data1.items():
            if key2 not in items:
                continue
            if "collision_box" not in data2 or "selection_box" not in data2:
                continue

            items[key2]["collision_box"] = data2["collision_box"]
            items[key2]["selection_box"] = data2["selection_box"]
            for key3 in data2.keys():
                pipe_connections = []
                if key3 == "fluid_boxes":
                    for fluid_box in data2[key3]:
                        pipe_connections.extend(fluid_box["pipe_connections"])      
                elif key3.endswith("fluid_box"):
                    pipe_connections.extend(data2[key3]["pipe_connections"])
                else:
                    continue
                
                if key2 not in item_to_pipe_target_positions:
                    item_to_pipe_target_positions[key2] = []

                for pipe_connection in pipe_connections:
                    if key2 == "pumpjack": # TODO: this is a special case, I'm not sure why pumpjack has multiple positions
                        pipe_connection["position"] = pipe_connection["positions"][0]

                    offset = DIRECTION_4_TO_OFFSET[pipe_connection["direction"]//4]
                    pos = pipe_connection["position"]
                    target_position = [pos[0] + offset[0], pos[1] + offset[1]]
                    item_to_pipe_target_positions[key2].append([pos, target_position])

            # Process heat connections from both energy_source and heat_buffer
            for heat_source in ['energy_source', 'heat_buffer']:
                if (heat_source in data2 and isinstance(data2[heat_source], dict) and 
                    "connections" in data2[heat_source]):
                    heat_connections = data2[heat_source]["connections"]
                    if key2 not in item_to_heat_target_positions:
                        item_to_heat_target_positions[key2] = []
                    
                    for connection in heat_connections:
                        offset = DIRECTION_4_TO_OFFSET[connection["direction"]//4]
                        pos = connection["position"]
                        target_position = [pos[0] + offset[0], pos[1] + offset[1]]
                        item_to_heat_target_positions[key2].append([pos, target_position])

# Remove items without collision box
items = {name: data for name, data in items.items() if "collision_box" in data}

# Sort items by group and subgroup
sorted_items = dict(sorted(items.items(), key=lambda x: (x[1]['group'], x[1]['subgroup'], x[0])))

# Prepare the JavaScript output
js_output = ["const entityNameToProperties = {"]
current_group = None
current_subgroup = None

for item_name, item_data in sorted_items.items():
    if item_data["group"] != current_group:
        js_output.append(f"\n    // Group: {item_data['group'].capitalize()}")
        current_group = item_data["group"]
    if item_data["subgroup"] != current_subgroup:
        js_output.append(f"    // Subgroup: {item_data['subgroup']}")
        current_subgroup = item_data["subgroup"]
    
    item_data['genericTerms'] = [item_data['group'], item_data['subgroup']]
    
    item_data['size'] = [item_data['collision_box'][1][0] - item_data['collision_box'][0][0], item_data['collision_box'][1][1] - item_data['collision_box'][0][1]]
    
    # Convert to JavaScript format
    props_str = "{ "
    props_str += f"selectionBox: {str(item_data['selection_box'])}, "
    props_str += f"collisionBox: {str(item_data['collision_box'])}, "
    props_str += f"size: {str(item_data['size'])}, "
    props_str += f"genericTerms: {str(item_data['genericTerms'])}"
    if "pipe_connection_target_positions" in item_data:
        props_str += f", pipeConnectionTargetPositions: {str(item_data['pipe_connection_target_positions'])}"
    props_str += " }"
    
    js_output.append(f'    "{item_name}": {props_str},')
js_output.append("}")

# Add item_to_pipe_target_positions to js_output
js_output.append("\n\nconst itemToPipeTargetPositions = {")
for item_name, positions in sorted(item_to_pipe_target_positions.items()):
    js_output.append(f'    "{item_name}": {str(positions)},')
js_output.append("}")

# Add item_to_heat_target_positions to js_output
js_output.append("\n\nconst itemToHeatTargetPositions = {")
for item_name, positions in sorted(item_to_heat_target_positions.items()):
    js_output.append(f'    "{item_name}": {str(positions)},')
js_output.append("}")

# Get recipes with fluid ingredients or results
fluid_crafting_recipes = []
for recipe in recipe_json['recipe'].values():
    has_fluid = False
    
    # Check ingredients
    if 'ingredients' in recipe:
        for ingredient in recipe['ingredients']:
            if isinstance(ingredient, dict) and ingredient.get('type') == 'fluid':
                has_fluid = True
                break
    
    # Check results
    if not has_fluid and 'results' in recipe:
        for result in recipe['results']:
            if isinstance(result, dict) and result.get('type') == 'fluid':
                has_fluid = True
                break
    
    if has_fluid:
        fluid_crafting_recipes.append(recipe['name'])

# Save fluid crafting recipes
js_output.append("\n\nconst fluidRecipes = {")
for recipe in sorted(fluid_crafting_recipes):
    js_output.append(f'    "{recipe}": true,')
js_output.append("}")

# Write to JavaScript file
with open('entity_properties.js', 'w') as file:
    file.write('\n'.join(js_output))

