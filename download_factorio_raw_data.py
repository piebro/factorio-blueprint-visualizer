# /// script
# dependencies = [
#   "requests",
#   "luadata",
# ]
# ///

import requests
import re
import luadata
import json
import os

def download_and_parse_data():
    # Download the data
    url = "https://gist.githubusercontent.com/Bilka2/6b8a6a9e4a4ec779573ad703d03c1ae7/raw"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download data: {response.status_code}")
    
    # Get the content
    content = response.text

    # Clean up the content to make it valid Lua
    # Remove the script header if present
    content = re.sub(r'^Script.*?: ', '', content)
    
    # Remove Lua multi-line comments
    content = re.sub(r'--\[=\[.*?\]=\]', '', content, flags=re.DOTALL)
    
    # Convert scientific notation to decimal notation
    def convert_scientific(match):
        num = float(match.group(0))
        return f"{num:.10f}".rstrip('0').rstrip('.')
    
    content = re.sub(r'-?\d+\.?\d*[eE][+-]?\d+', convert_scientific, content)
    
    # Remove any trailing commas in arrays/tables
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Ensure proper line endings
    content = content.replace('\r\n', '\n')
    
    try:
        a = luadata.unserialize(content, encoding="utf-8", multival=False)
        return a
    except Exception as e:
        print(f"Error position in content: {str(e)}")
        # Save problematic content to a file for inspection
        with open('debug_lua_content.txt', 'w') as f:
            f.write(content)
        raise

def remove_layers_recursively(data):
    if isinstance(data, dict):
        # Remove 'layers' and 'sprites' keys if present
        data.pop('layers', None)
        data.pop('sprites', None)
        # Recursively process all values
        for value in data.values():
            remove_layers_recursively(value)
    elif isinstance(data, list):
        # Recursively process all items in list
        for item in data:
            remove_layers_recursively(item)
    return data

if __name__ == "__main__":
    data = download_and_parse_data()
    data.pop('achievement', None)
    data.pop('technology', None)
    data.pop('tips-and-tricks-item', None)
    data.pop('rail-planner', None)

    recipe_data = {
        'recipe': data.pop('recipe', {}),
        'recipe-category': data.pop('recipe-category', {})
    }

    item_data = {
        'item': data.pop('item', {}),
        'item-group': data.pop('item-group', {}),
        'item-subgroup': data.pop('item-subgroup', {}),
    }

    filtered_keys = [
        'accumulator',
        'agricultural-tower',
        'arithmetic-combinator',
        'assembling-machine',
        'asteroid-collector',
        'beacon',
        'boiler',
        'burner-generator',
        'cargo-bay',
        'cargo-landing-pad',
        'constant-combinator',
        'container',
        'curved-rail-a',
        'curved-rail-b',
        'decider-combinator',
        'electric-pole',
        'electric-turret',
        'elevated-curved-rail-a',
        'elevated-curved-rail-b',
        'elevated-half-diagonal-rail',
        'elevated-straight-rail',
        'fluid-turret',
        'furnace',
        'fusion-generator',
        'fusion-reactor',
        'gate',
        'generator',
        'half-diagonal-rail',
        'heat-interface', # TODO: check if this is needed
        'heat-pipe',
        'highlight-box',
        'inserter',
        'lab',
        'lamp',
        'lightning-attractor',
        'logistic-container',
        'mining-drill',
        'offshore-pump',
        'pipe',
        'pipe-to-ground',
        'power-switch',
        'programmable-speaker',
        'pump',
        'radar',
        'rail-chain-signal',
        'rail-ramp',
        'rail-remnants', # TODO: check if this is needed
        'rail-signal',
        'rail-support',
        'reactor',
        'roboport',
        'rocket-silo',
        'selector-combinator',
        'solar-panel',
        'splitter',
        'storage-tank',
        'straight-rail',
        'thruster',
        'train-stop',
        'transport-belt',
        'underground-belt',
        'wall'
    ]
    filtered_data = {key: data[key] for key in filtered_keys}

    filtered_data = data

    filtered_data = remove_layers_recursively(filtered_data)
    
    
    
    # Create factorio_data directory if it doesn't exist
    os.makedirs('factorio_data', exist_ok=True)
    
    # Extract recipe-related data
    

    print(data.keys())
    
    # Save recipe data to a separate file
    with open('factorio_data/recipe_data.json', 'w', encoding='utf-8') as f:
        json.dump(recipe_data, f, indent=2, ensure_ascii=False)
    print(f"Recipe data saved to factorio_data/recipe_data.json")

    # Save item data to a separate file
    with open('factorio_data/item_data.json', 'w', encoding='utf-8') as f:
        json.dump(item_data, f, indent=2, ensure_ascii=False)
    print(f"Item data saved to factorio_data/item_data.json")
    
    # Save remaining data
    with open('factorio_data/factorio_data.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    print(f"Main data saved to factorio_data/factorio_data.json")