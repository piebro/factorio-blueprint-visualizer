# python file only for the demo website

# building_settings

NORTH = 0
NORTH_EAST = 1
EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7

BUILDING_SIZES = {
    # first tab: Logistics
    "wooden-chest": (1,1),
    "iron-chest": (1,1),
    "steel-chest": (1,1),
    "storage-tank": (3,3),

    "transport-belt": (1,1),
    "fast-transport-belt": (1,1),
    "express-transport-belt": (1,1),
    "underground-belt": (1,1),
    "fast-underground-belt": (1,1),
    "express-underground-belt": (1,1),
    "splitter": (2,1),
    "fast-splitter": (2,1),
    "express-splitter": (2,1),

    "burner-inserter": (1,1),
    "inserter": (1,1),
    "long-handed-inserter": (1,1),
    "fast-inserter": (1,1),
    "filter-inserter": (1,1),
    "stack-inserter": (1,1),
    "stack-filter-inserter": (1,1),

    "small-electric-pole": (1,1),
    "medium-electric-pole": (1,1),
    "big-electric-pole": (2,2),
    "substation": (2,2),
    "pipe": (1,1),
    "pipe-to-ground": (1,1),
    "pump": (1,2),

    "straight-rail": (2,2),
    "curved-rail": (2,2),
    "train-stop": (2,2),
    "rail-signal": (1,1),
    "rail-chain-signal": (1,1),

    "logistic-chest-active-provider": (1,1),
    "logistic-chest-passive-provider": (1,1),
    "logistic-chest-storage": (1,1),
    "logistic-chest-buffer": (1,1),
    "logistic-chest-requester": (1,1),
    "roboport": (4,4),

    "small-lamp": (1,1),
    "arithmetic-combinator": (1,2),
    "decider-combinator": (1,2),
    "constant-combinator": (1,1),
    "power-switch": (2,2),
    "programmable-speaker": (1,1),

    # tap 2
    "boiler": (3, 2),
    "steam-engine": (3,5), ####
    "solar-panel": (3,3),
    "accumulator": (2,2),
    "nuclear-reactor": (5,5),
    "heat-pipe": (1,1),
    "heat-exchanger": (3,2),
    "steam-turbine": (3,5),

    "burner-mining-drill": (2,2),
    "electric-mining-drill": (3,3),
    "offshore-pump": (1, 2),
    "pumpjack": (3,3),

    "stone-furnace": (2,2),
    "steel-furnace": (2,2),
    "electric-furnace": (3,3),

    "assembling-machine-1": (3,3),
    "assembling-machine-2": (3,3),
    "assembling-machine-3": (3,3),
    "oil-refinery": (5,5),
    "chemical-plant": (3,3),
    "centrifuge": (3,3),
    "lab": (3,3),

    "beacon": (3,3),
    "rocket-silo": (9,9),

    # tap 3
    "stone-wall": (1,1),
    "gate": (1,1),
    "gun-turret": (2,2),
    "laser-turret": (2,2),
    "flamethrower-turret": (2,3),
    "artillery-turret": (3,3),
    "radar": (3,3),

    ### MODS
    # Factorissimo2
    "factory-1":(8,8),
    "factory-2":(12,12),
    "factory-3":(16,16),
    "factory-circuit-input": (1,1),
    "factory-circuit-output": (1,1),
    "factory-input-pipe": (1,1),
    "factory-output-pipe": (1,1),
    "factory-requester-chest": (1,1),
}

BUILDING_GENERIC_TERMS = {
    "assembling-machine": ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"],
    "producing-machines": ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3", "oil-refinery",
                           "chemical-plant", "centrifuge"],
    "belt-stuff": ["transport-belt", "fast-transport-belt", "express-transport-belt", "underground-belt",
                   "fast-underground-belt", "express-underground-belt", "splitter", "fast-splitter",
                   "express-splitter"],
    "electric-stuff": ["small-electric-pole", "medium-electric-pole", "big-electric-pole", "substation"],
    "furnace": ["stone-furnace", "steel-furnace", "electric-furnace"],
    "drill": ["burner-mining-drill", "electric-mining-drill", "pumpjack"],
    "electicity-generation": ["steam-engine", "solar-panel", "nuclear-reactor", "steam-turbine"],
    "military": ["stone-wall", "gate", "gun-turret", "laser-turret", "flamethrower-turret", "artillery-turret",
                 "radar"],
    "all-inserter": ["burner-inserter", "inserter", "long-handed-inserter", "fast-inserter", "filter-inserter",
                     "stack-inserter", "stack-filter-inserter"],
    "chests": ["wooden-chest", "iron-chest", "steel-chest", "logistic-chest-active-provider",
               "logistic-chest-passive-provider", "logistic-chest-storage", "logistic-chest-buffer",
               "logistic-chest-requester"],
    "rail": ["straight-rail", "curved-rail"],
    "connected-stuff": ["transport-belt", "fast-transport-belt", "express-transport-belt", "underground-belt",
                  "fast-underground-belt", "express-underground-belt", "splitter", "fast-splitter", "express-splitter",
                  "straight-rail", "curved-rail", "pipe", "pipe-to-ground", "burner-inserter", "inserter",
                  "long-handed-inserter", "fast-inserter", "filter-inserter", "stack-inserter",
                  "stack-filter-inserter"],
    "train-stuff": ["straight-rail", "curved-rail", "train-stop", "rail-signal", "rail-chain-signal"],

    ### MODS
    # Factorissimo2
    "factorissimo2": ["factory-1", "factory-2", "factory-3", "factory-circuit-input", "factory-circuit-output", "factory-input-pipe", "factory-output-pipe", "factory-requester-chest"],
}

RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE = {
  "electric-engine-unit": NORTH,
  "express-transport-belt": NORTH,
  "express-underground-belt": NORTH,
  "express-splitter": NORTH,
  "rocket-fuel": NORTH,
  "processing-unit": NORTH,
  "fill-crude-oil-barrel": NORTH,
  "empty-crude-oil-barrel": SOUTH,
  "fill-heavy-oil-barrel": NORTH,
  "empty-heavy-oil-barrel": SOUTH,
  "fill-light-oil-barrel": NORTH,
  "empty-light-oil-barrel": SOUTH,
  "fill-lubricant-barrel": NORTH,
  "empty-lubricant-barrel": SOUTH,
  "fill-petroleum-gas-barrel": NORTH,
  "empty-petroleum-gas-barrel": SOUTH,
  "fill-sulfuric-acid-barrel": NORTH,
  "empty-sulfuric-acid-barrel": SOUTH,
  "fill-water-barrel": NORTH,
  "empty-water-barrel": SOUTH,
}

BUILDING_PIPE_CONNECTIONS = {
    "pipe":[
      {"pos":(0,0), "direction": NORTH},
      {"pos":(0,0), "direction": EAST},
      {"pos":(0,0), "direction": SOUTH},
      {"pos":(0,0), "direction": WEST}      
    ],
    "assembling-machine-1":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "assembling-machine-2":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "assembling-machine-3":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "boiler":[
      {"pos":(0,-0.5), "direction": NORTH},
      {"pos":(1,0.5), "direction": EAST},
      {"pos":(-1,0.5), "direction": WEST}
    ],
    "pipe-to-ground":[
      {"pos":(0,0), "direction": NORTH}
    ],
    "offshore-pump":[
      {"pos":(0,0.5), "direction": SOUTH}
    ],
    "steam-engine":[
      {"pos":(0,-2), "direction": NORTH},
      {"pos":(0,2), "direction": SOUTH}
    ],
    "oil-refinery":[
      {"pos":(-2,-2), "direction": NORTH},
      {"pos":(0,-2), "direction": NORTH},
      {"pos":(2,-2), "direction": NORTH},
      {"pos":(-1,2), "direction": SOUTH},
      {"pos":(1,2), "direction": SOUTH}
    ],
    "chemical-plant":[
      {"pos":(-1,-1), "direction": NORTH},
      {"pos":(1,-1), "direction": NORTH},
      {"pos":(-1,1), "direction": SOUTH},
      {"pos":(1,1), "direction": SOUTH}
    ],
}



# draw.py

import numpy as np

def get_drawing(bbox_width, bbox_height, max_size_in_mm=250, background_color="#dddddd", settings=None):
  if bbox_width>bbox_height:
    dwg_size_in_mm = (max_size_in_mm, np.round(max_size_in_mm*bbox_height/bbox_width))
  else:
    dwg_size_in_mm = (np.round(max_size_in_mm*bbox_width/bbox_height), max_size_in_mm)

  dwg = [f'<svg baseProfile="tiny" height="{dwg_size_in_mm[1]}mm" version="1.2" viewBox="0,0,{bbox_width},{bbox_height}" width="{dwg_size_in_mm[0]}mm" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">']

  if settings is not None:
    dwg.append(f"<metadata><generated_with>https://piebro.github.io/factorio-blueprint-visualizer/</generated_with><settings>{settings}</settings></metadata>")

  if background_color is not None:
    dwg.append(f'<rect fill="{background_color}" height="10000" width="10000" x="-100" y="-100" />')
  return dwg

def draw_lines(dwg, lines, svg_setting):
  dwg.append('<path')
  append_svg_setting(dwg, svg_setting)
  dwg.append(' d="')
  for p1, p2 in lines:
    dwg.append('M{} {} {} {}'.format(*p1, *p2))
  dwg.append('"/>')

def append_svg_setting(dwg, svg_setting, deny_list=[]):
  for key, value in svg_setting.items():
    if key not in deny_list:
      dwg.append(f' {key}="{value}"')

def append_group(dwg, svg_setting, deny_list=[]):
  dwg.append('<g')
  append_svg_setting(dwg, svg_setting, deny_list)
  dwg.append('>')

def draw_rect(dwg, mid, size, scale, rx, ry):
  if scale is not None:
    size = (size[0] * scale, size[1] * scale)

  dwg.append(f'<rect height="{size[1]}" width="{size[0]}" x="{mid[0]-size[0]/2}" y="{mid[1]-size[1]/2}"')
  
  if rx is not None:
    dwg.append(f' rx="{rx}" ')
  if ry is not None:
    dwg.append(f' ry="{ry}" ')

  dwg.append('/>')


# factorio_blueprint_visualizer.py

import json
import zlib
import base64
import random
import os
import re

#import numpy as np

#from building_settings import BUILDING_SIZES, BUILDING_GENERIC_TERMS, RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE, BUILDING_PIPE_CONNECTIONS

#from draw import get_drawing, draw_lines, draw_rect, append_group

DIRECTION_OFFSET = np.array([[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]])


def add_blueprint(blueprint_dict, blueprint_string):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(blueprint_string[1:])))  
  get_label_and_blueprint(blueprint_dict, "", raw_blueprint_json)
  return list(blueprint_dict.keys())

def get_label_and_blueprint(blueprint_dict, raw_blueprint_json):
  if "blueprint" in raw_blueprint_json:
    if "label" in raw_blueprint_json["blueprint"]:
      label = raw_blueprint_json['blueprint']['label']
    else:
      label = f"{random.randrange(0, 10000):05d}"
    
    blueprint_dict[label] = raw_blueprint_json["blueprint"]

  elif "blueprint_book" in raw_blueprint_json:

    for raw_blueprint in raw_blueprint_json["blueprint_book"]["blueprints"]:
      get_label_and_blueprint(blueprint_dict, raw_blueprint)

def get_label_and_blueprint_with_pre_string(blueprint_dict, pre_string, raw_blueprint_json):
  if "blueprint" in raw_blueprint_json:
    if "label" in raw_blueprint_json["blueprint"]:
      label = raw_blueprint_json['blueprint']['label']
    else:
      label = f"{random.randrange(0, 10000):05d}"
    if pre_string != "":
      label = pre_string + "-" + label

    blueprint_dict[label] = raw_blueprint_json["blueprint"]
  elif "blueprint_book" in raw_blueprint_json:
    if "label" in raw_blueprint_json["blueprint_book"]:
      label = raw_blueprint_json['blueprint_book']['label']
    else:
      label = ""
    
    if pre_string != "" and label != "":
      label = pre_string + "-" + label

    for raw_blueprint in raw_blueprint_json["blueprint_book"]["blueprints"]:
      get_label_and_blueprint_with_pre_string(blueprint_dict, label, raw_blueprint)

def get_simplified_entities(blueprint_json):
  if "entities" not in blueprint_json:
    return []

  for e in blueprint_json["entities"]:
    if "direction" not in e:
      e["direction"] = 0
    e["direction"] = int(e["direction"])

    e["pos"] = np.array([float(e["position"]["x"]), float(e["position"]["y"])])
    if e["name"] == "offshore-pump":
      e["pos"] += 0.5*DIRECTION_OFFSET[e["direction"]]
  return blueprint_json["entities"]

def get_size_and_normalize_entities(entities, bbox_border, building_sizes):
  if len(entities) == 0:
    return 1, 1
  entity_bboxes = []
  for e in entities:
    if e["name"] in building_sizes:
      if e["direction"]%2 == 0:
        size_x, size_y = building_sizes[e["name"]]
      else:
        size_y, size_x = building_sizes[e["name"]]
      entity_bboxes.append((e["pos"][0]-size_x/2, e["pos"][1]-size_y/2, e["pos"][0]+size_x/2, e["pos"][1]+size_y/2))
  entity_bboxes = np.array(entity_bboxes)

  bbox = np.array([np.min(entity_bboxes[:, 0]), np.min(entity_bboxes[:, 1]), np.max(entity_bboxes[:, 2]), np.max(entity_bboxes[:, 3])])
  bbox += np.array([-bbox_border, -bbox_border, bbox_border, bbox_border])
  bbox_width = bbox[2]-bbox[0] 
  bbox_height = bbox[3]-bbox[1]

  for e in entities:
    if "pos" in e:
      e["pos"] -= bbox[:2]

  return bbox_width, bbox_height

def sort_entities(entities, order):
  sort_index = []
  for e in entities:
    if e["name"] in order:
      sort_index.append(-order.index(e["name"]))
    else:
      sort_index.append(-order.index("rest"))

  return [x for _,x in sorted(zip(sort_index, entities), key=lambda pair: pair[0])]

def rotate(angle, pos):
  if angle==0:
    return pos
  elif angle==2:
    return (-pos[1], pos[0])
  elif angle==4:
    return (-pos[0], -pos[1])
  elif angle==6:
    return (pos[1], -pos[0])

def add_pos_to_nodes(nodes, pos, dir):
  if pos not in nodes:
    nodes[pos] = [False, False, False, False, False, False, False, False]
  nodes[pos][dir] = True


def get_lines_inserter(dwg, entities):
  lines = []
  for e in entities:
    if e["name"] in ["burner-inserter", "inserter", "fast-inserter", "filter-inserter", "stack-inserter", "stack-filter-inserter"]:
      p0 = e["pos"] + DIRECTION_OFFSET[e["direction"]]
      p1 = e["pos"] - DIRECTION_OFFSET[e["direction"]]
      lines.append([p0, p1])
    elif e["name"] in ["long-handed-inserter"]:
      p0 = e["pos"] + 2*DIRECTION_OFFSET[e["direction"]]
      p1 = e["pos"] - 2*DIRECTION_OFFSET[e["direction"]]
      lines.append([p0, p1])
  return lines

def get_lines_nodes_and_connect_conditions(nodes, connect_conditions, draw_nodes=False, draw_target_pos=False, set_self_false=True, set_target_false=True):
  if draw_nodes:
    lines = [[pos, pos] for pos in nodes]
    if draw_target_pos:
      lines.extend([[target_pos, target_pos] for _, _, target_pos, _ in connect_conditions])
    return lines
  lines = []
  for src_pos, src_dir, target_pos, target_dir in connect_conditions:
    if nodes[src_pos][src_dir] and target_pos in nodes and nodes[target_pos][target_dir]:
      lines.append([src_pos, target_pos])
      nodes[target_pos][target_dir] = not set_self_false
      nodes[src_pos][src_dir] = not set_target_false
  return lines

def get_lines_pipes(dwg, entities, building_pipe_connections, recipes_in_assembly_machine_with_fluids_to_dir_change):
  nodes = {}
  connect_conditions = []
  for e in entities:
    if e["name"] not in building_pipe_connections:
      continue
      
    if e["name"] in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
      if "recipe" not in e:
        continue

      if e["recipe"] in recipes_in_assembly_machine_with_fluids_to_dir_change:
        recipe_dir_change = recipes_in_assembly_machine_with_fluids_to_dir_change[e["recipe"]]
      else:
        continue
    else:
      recipe_dir_change = 0

    for connection in building_pipe_connections[e["name"]]:
      pos = tuple(e["pos"] + rotate((e["direction"] + recipe_dir_change)%8, connection["pos"]))
      dir = (e["direction"] + connection["direction"] + recipe_dir_change)%8
      add_pos_to_nodes(nodes, tuple(pos), dir)

      target_pos = tuple(np.array(pos) + DIRECTION_OFFSET[dir])
      target_dir = (dir+4)%8
      connect_conditions.append([pos, dir, target_pos, target_dir])

  return get_lines_nodes_and_connect_conditions(nodes, connect_conditions)

def get_lines_underground_pipes(dwg, entities, max_length):
  nodes = {}
  for e in entities:
    if e["name"] == "pipe-to-ground":
      nodes[tuple(e["pos"])] = (e["direction"]+4)%8
  
  lines = []
  for pos, dir in nodes.items():
    if dir < 4:
      dir_offset = DIRECTION_OFFSET[dir]
      for i in range(1, max_length):
        target_pos = tuple(np.array(pos) + i*dir_offset)
        if target_pos in nodes and nodes[target_pos] == (dir+4)%8:
          lines.append([pos, target_pos])
          break
  return lines

def get_lines_belt(dwg, entities):
  nodes = {}
  connect_conditions = []
  for e in entities:
    if e["name"] in ["transport-belt", "fast-transport-belt", "express-transport-belt", "underground-belt", "fast-underground-belt", "express-underground-belt"]:
      pos = tuple(e["pos"])
      dir = e["direction"]
      add_pos_to_nodes(nodes, pos, dir)
      
      if "type" in e and e["type"]=="input":
        continue

      target_pos = tuple(np.array(pos) + DIRECTION_OFFSET[dir])
      for target_dir in [(dir-2)%8, dir, (dir+2)%8]:
        connect_conditions.append([pos, dir, target_pos, target_dir])

    elif e["name"] in ["splitter", "fast-splitter", "express-splitter"]:
      dir = e["direction"]
      offset = 0.5*DIRECTION_OFFSET[(dir+2)%8]
      pos_1_2 = [tuple(e["pos"]-offset), tuple(e["pos"]+offset)]

      for pos in pos_1_2:
        add_pos_to_nodes(nodes, pos, dir)
      
        for pos_i in [0,1]:
            target_pos = tuple(np.array(pos_1_2[pos_i]) + DIRECTION_OFFSET[dir])
            for target_dir in [(dir-2)%8, dir, (dir+2)%8]:
              connect_conditions.append([pos, dir, target_pos, target_dir])

  return get_lines_nodes_and_connect_conditions(nodes, connect_conditions, draw_nodes=False, set_self_false=False, set_target_false=False)

def get_lines_underground_belt(dwg, entities, entity_name, max_length):
  nodes_input = {}
  nodes_output = {}
  for e in entities:
    if e["name"] == entity_name:
      if e["type"] == "input":
        nodes_input[tuple(e["pos"])] = e["direction"]
      else:
        nodes_output[tuple(e["pos"])] = e["direction"]
  
  lines = []
  for pos, dir in nodes_input.items():
    dir_offset = DIRECTION_OFFSET[dir]
    for i in range(1, max_length):
      target_pos = tuple(np.array(pos) + i*dir_offset)
      if target_pos in nodes_output and nodes_output[target_pos] == dir:
        lines.append([pos, target_pos])
        break

  return lines

def get_lines_rails(dwg, entities):
  lines = []
  for e in entities:
    if e["name"] == "straight-rail":
      dir = e["direction"]
      if dir%2==0:
        p0 = e["pos"] + DIRECTION_OFFSET[dir]
        p1 = e["pos"] - DIRECTION_OFFSET[dir]
        lines.append([p0, p1])
      else:
        p0 = e["pos"] + DIRECTION_OFFSET[(dir-1)%8]
        p1 = e["pos"] + DIRECTION_OFFSET[(dir+1)%8]
        lines.append([p0, p1])
    elif e["name"] == "curved-rail":
      pos = e["pos"]
      dir = e["direction"]
      if dir%2==0:
        lines.append([pos+rotate(dir, np.array([-2,-3])), pos])
        lines.append([pos, pos+rotate(dir, np.array([1,4]))])
      elif dir%2==1:
        lines.append([pos + rotate(dir-1, np.array([2,-3])), pos])
        lines.append([pos, pos+rotate(dir-1, np.array([-1,4]))])

  return lines


def replace_building_generic_terms(builing_name_list, building_generic_terms):
  new_builing_name_list = []
  for name in builing_name_list:
    if name in building_generic_terms:
      new_builing_name_list.extend(building_generic_terms[name])
    else:
      new_builing_name_list.append(name)
  return new_builing_name_list

def draw_entities_bbox(dwg, entities, settings, default_bbox_prop, building_sizes, building_generic_terms):
  if "allow" in settings:
    bbox_entities = [e for e in entities if e["name"] in replace_building_generic_terms(settings["allow"], building_generic_terms)]
  elif "deny" in settings:
    bbox_entities = [e for e in entities if e["name"] not in replace_building_generic_terms(settings["deny"], building_generic_terms)]
  else:
    bbox_entities = entities
    
  bbox_prop = {}
  for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
    if bbox_prop_key in settings:
      bbox_prop[bbox_prop_key[5:]] = settings[bbox_prop_key]
    else:
      bbox_prop[bbox_prop_key[5:]] = default_bbox_prop[bbox_prop_key[5:]]

  append_group(dwg, settings, deny_list=["bbox-scale", "bbox-rx", "bbox-ry"])
  for e in bbox_entities:
    if e["name"] in building_sizes:
      if e["direction"]%4 == 0:
        size_x, size_y = building_sizes[e["name"]]
      else:
        size_y, size_x = building_sizes[e["name"]]
      draw_rect(dwg, e["pos"], (size_x, size_y), **bbox_prop)
  dwg.append('</g>')

def get_blueprint_labels(encoded_blueprint_str):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  blueprint_dict = {}
  get_label_and_blueprint(blueprint_dict, raw_blueprint_json)
  return list(blueprint_dict.keys())


def get_blueprint_cache(encoded_blueprint_str, blueprint_name_or_number, bbox_border=3, building_settings={}):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  
  building_sizes = building_settings["BUILDING_SIZES"] if "BUILDING_SIZES" in building_settings else BUILDING_SIZES

  blueprint_dict = {}
  get_label_and_blueprint(blueprint_dict, raw_blueprint_json)

  if isinstance(blueprint_name_or_number, str):
    blueprint_name = blueprint_name_or_number
  else:
    blueprint_name = list(blueprint_dict.keys())[blueprint_name_or_number]

  entities = get_simplified_entities(blueprint_dict[blueprint_name])
  bbox_width, bbox_height = get_size_and_normalize_entities(entities, bbox_border, building_sizes)
  cache = {"bbox_width": bbox_width, "bbox_height": bbox_height, "entities": entities}
  return cache

def get_custom_building_settings(new_building_sizes={}, new_building_generic_terms={}, new_building_pipe_connections={}, new_recipes_in_assembly_machine_with_fluids_to_dir_change={}):
  custom_building_settings = {}
  custom_building_settings["BUILDING_SIZES"] = {**BUILDING_SIZES, **new_building_sizes}
  custom_building_settings["BUILDING_GENERIC_TERMS"] = {**BUILDING_GENERIC_TERMS, **new_building_generic_terms}
  custom_building_settings["BUILDING_PIPE_CONNECTIONS"] = {**BUILDING_PIPE_CONNECTIONS, **new_building_pipe_connections}
  custom_building_settings["RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE"] = {**RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE, **new_recipes_in_assembly_machine_with_fluids_to_dir_change}
  return custom_building_settings

def draw_blueprints(encoded_blueprint_str, blueprint_name_or_number, settings, blueprint_cache=None, svg_max_size_in_mm=300, building_settings={}):

  building_sizes = building_settings["BUILDING_SIZES"] if "BUILDING_SIZES" in building_settings else BUILDING_SIZES
  building_generic_terms = building_settings["BUILDING_GENERIC_TERMS"] if "BUILDING_GENERIC_TERMS" in building_settings else BUILDING_GENERIC_TERMS
  
  if "BUILDING_SIZES" in building_settings:
    building_sizes = building_settings["BUILDING_SIZES"]
  else:
    building_sizes = BUILDING_SIZES

  if "BUILDING_GENERIC_TERMS" in building_settings:
    building_generic_terms = building_settings["BUILDING_GENERIC_TERMS"]
  else:
    building_generic_terms = BUILDING_GENERIC_TERMS

  if "BUILDING_PIPE_CONNECTIONS" in building_settings:
    building_pipe_connections = building_settings["BUILDING_PIPE_CONNECTIONS"]
  else:
    building_pipe_connections = BUILDING_PIPE_CONNECTIONS
  
  if "RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE" in building_settings:
    recipes_in_assembly_machine_with_fluids_to_dir_change = building_settings["RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE"]
  else:
    recipes_in_assembly_machine_with_fluids_to_dir_change = RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE

  default_meta_settings = {"background":"#E6E6E6"}
  if settings[0][0] == "meta":
    meta_settings = {**default_meta_settings, **settings[0][1]}
  else:
    meta_settings = default_meta_settings
  
  if blueprint_cache is None:
    blueprint_cache = get_blueprint_cache(encoded_blueprint_str, blueprint_name_or_number, bbox_border=3)
  entities = blueprint_cache["entities"]

  dwg = get_drawing(blueprint_cache["bbox_width"], blueprint_cache["bbox_height"], svg_max_size_in_mm, meta_settings["background"], settings)  
  dwg_groups_to_close = 0
  default_bbox_prop = {"scale": None, "rx": None, "ry": None}
  
  for setting in settings:
    if setting[0] == "default-svg-properties":
      append_group(dwg, setting[1], deny_list=["bbox-scale", "bbox-rx", "bbox-ry"])
      dwg_groups_to_close += 1
      for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
        if bbox_prop_key in setting[1]:
          default_bbox_prop[bbox_prop_key[5:]] = setting[1][bbox_prop_key]
      
    elif setting[0] == "bbox":
      draw_entities_bbox(dwg, entities, setting[1], default_bbox_prop, building_sizes, building_generic_terms)
      
    elif setting[0] == "connected-belt":
      if "connected-belt" not in blueprint_cache:
        blueprint_cache["connected-belt"] = get_lines_belt(dwg, entities)
      draw_lines(dwg, blueprint_cache["connected-belt"], setting[1])

    elif setting[0] == "connected-underground-belt":
      if "connected-underground-belt" not in blueprint_cache:
        lines = get_lines_underground_belt(dwg, entities, "underground-belt", 6)
        lines.extend(get_lines_underground_belt(dwg, entities, "fast-underground-belt", 8))
        lines.extend(get_lines_underground_belt(dwg, entities, "express-underground-belt", 10))
        blueprint_cache["connected-underground-belt"] = lines
      draw_lines(dwg, blueprint_cache["connected-underground-belt"], setting[1])

    elif setting[0] == "connected-pipe-to-ground":
      if "connected-pipe-to-ground" not in blueprint_cache:
        blueprint_cache["connected-pipe-to-ground"] = get_lines_underground_pipes(dwg, entities, 11)
      draw_lines(dwg, blueprint_cache["connected-pipe-to-ground"], setting[1])

    elif setting[0] == "connected-pipe":
      if "connected-pipe" not in blueprint_cache:
        blueprint_cache["connected-pipe"] = get_lines_pipes(dwg, entities, building_pipe_connections, recipes_in_assembly_machine_with_fluids_to_dir_change)
      draw_lines(dwg, blueprint_cache["connected-pipe"], setting[1])
  
    elif setting[0] == "connected-inserter":
      if "connected-inserter" not in blueprint_cache:
        blueprint_cache["connected-inserter"] = get_lines_inserter(dwg, entities)
      draw_lines(dwg, blueprint_cache["connected-inserter"], setting[1])

    elif setting[0] == "connected-rail":
      if "connected-rail" not in blueprint_cache:
        blueprint_cache["connected-rail"] = get_lines_rails(dwg, entities)
      draw_lines(dwg, blueprint_cache["connected-rail"], setting[1])

  for _ in range(dwg_groups_to_close):
    dwg.append('</g>')
  dwg.append("</svg>")
  return "".join(dwg)


def check_for_filename(folder_path, filename, file_ending):
  if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
  
  files_in_folder = os.listdir(folder_path)
  for i in range(10000):
    possible_valid_fn = f"{filename}_{i:05d}.{file_ending}"
    if possible_valid_fn not in files_in_folder:
      return os.path.join(folder_path, possible_valid_fn)

def get_settings_from_svg(svg_path):
  with open(svg_path, 'r') as txt_file:
    settings_svg_str = txt_file.read()
  settings_str = re.findall(r"<settings>(.*)</settings>", settings_svg_str)[0]
  settings_str = settings_str.replace("'", "\"")
  return json.loads(settings_str)

def save_svg(folder_path, filename, svg_str):
  valid_file_path = check_for_filename(folder_path, filename, "svg")
  with open(valid_file_path, "w") as text_file:
    text_file.write(svg_str)
  print("saved at:", valid_file_path)


# random_settings.py

import copy
#import numpy as np

# generated with https://coolors.co/
PREDEFINED_COLOR_PALETTES = [
  [
    ['#2d7dd2', '#97cc04'],
    ['#6d213c', '#946846'],
    ['#54457f', '#ac7b84'],
    ['#0d3b66', '#faf0ca'],
    ['#1446a0', '#db3069'],
    ['#ff6666', '#ccff66'],
    ['#251605', '#c57b57'],
  ],[
    ['#ff4e00', '#8ea604', '#f5bb00'],
    ['#a54657', '#582630', '#f7ee7f'],
    ['#464d77', '#36827f', '#f9db6d'],
    ['#264653', '#2a9d8f', '#e9c46a'],
    ['#ef767a', '#456990', '#49beaa'],
    ['#eca400', '#eaf8bf', '#006992'],
    ['#ef946c', '#c4a77d', '#70877f'],
  ],[
    ['#ec0b43', '#58355e', '#7ae7c7', '#d6ffb7'],
    ['#bfae48', '#5fad41', '#2d936c', '#391463'],
    ['#c9cba3', '#ffe1a8', '#e26d5c', '#723d46'],
    ['#d7263d', '#02182b', '#0197f6', '#448fa3'],
    ['#042a2b', '#5eb1bf', '#cdedf6', '#ef7b45'],
    ['#540d6e', '#ee4266', '#ffd23f', '#f3fcf0'],
    ['#ffb997', '#f67e7d', '#843b62', '#0b032d'],
  ],[
    ['#d6ffb7', '#f5ff90', '#ffc15e', '#ff9f1c', '#080357'],
    ['#52489c', '#4062bb', '#59c3c3', '#ebebeb', '#f45b69'],
    ['#ee6055', '#60d394', '#aaf683', '#ffd97d', '#ff9b85'],
    ['#55dde0', '#33658a', '#2f4858', '#f6ae2d', '#f26419'],
    ['#fcde9c', '#ffa552', '#ba5624', '#381d2a', '#c4d6b0'],
    ['#1c3144', '#d00000', '#ffba08', '#a2aebb', '#3f88c5'],
    ['#acf39d', '#e85f5c', '#9cfffa', '#773344', '#e3b5a4'],
  ],[
    ['#6dd3ce', '#c8e9a0', '#f7a278', '#a13d63', '#351e29', '#2e282a'],
    ['#74b3ce', '#508991', '#172a3a', '#004346', '#09bc8a', '#bda0bc'],
    ['#6f1d1b', '#bb9457', '#432818', '#99582a', '#ffe6a7', '#020887'],
    ['#6d213c', '#946846', '#baab68', '#e3c16f', '#faff70', '#ffa9e7'],
    ['#bfb48f', '#564e58', '#904e55', '#f2efe9', '#252627', '#97dffc'],
    ['#0fa3b1', '#d9e5d6', '#eddea4', '#f7a072', '#ff9b42', '#e08dac'],
    ['#52414c', '#596157', '#5b8c5a', '#cfd186', '#e3655b', '#d67ab1'],
  ],[
    ['#58355e', '#e03616', '#fff689', '#cfffb0', '#5998c5', '#8eb1c7', '#12eaea'],
    ['#abe188', '#f7ef99', '#f1bb87', '#f78e69', '#5d675b', '#13293d', '#006494'],
    ['#2f4b26', '#3e885b', '#85bda6', '#bedcfe', '#c0d7bb', '#62466b', '#45364b'],
    ['#212738', '#f97068', '#d1d646', '#edf2ef', '#57c4e5', '#8b85c1', '#d4cdf4'],
    ['#fcde9c', '#ffa552', '#ba5624', '#381d2a', '#c4d6b0', '#adaabf', '#020402'],
    ['#e3e7af', '#a2a77f', '#eff1c5', '#035e7b', '#002e2c', '#c9b1bd', '#2e0219'],
    ['#9cfffa', '#acf39d', '#b0c592', '#a97c73', '#af3e4d', '#4281a4', '#c1666b'],
  ],[
    ['#247ba0', '#70c1b3', '#b2dbbf', '#f3ffbd', '#ff1654', '#436436', '#c84c09', '#420217'],
    ['#f0b67f', '#fe5f55', '#d6d1b1', '#c7efcf', '#eef5db', '#9d44b5', '#525252', '#272727'],
    ['#c0caad', '#9da9a0', '#654c4f', '#b26e63', '#cec075', '#00120b', '#35605a', '#004346'],
    ['#f2c57c', '#ddae7e', '#7fb685', '#426a5a', '#ef6f6c', '#466365', '#c4c6e7', '#baa5ff'],
    ['#87b38d', '#22031f', '#cc76a1', '#dd9296', '#f2b7c6', '#d17b0f', '#247ba0', '#449dd1'],
    ['#a20021', '#f52f57', '#f79d5c', '#f3752b', '#ededf4', '#048a81', '#06d6a0', '#54c6eb'],
    ['#d9e5d6', '#00a7e1', '#eddea4', '#f7a072', '#ff9b42', '#426a5a', '#ef6f6c', '#e05263'],
  ],[
    ['#b2aa8e', '#0c1b33', '#7a306c', '#03b5aa', '#dbfe87', '#a44200', '#3a5743', '#226ce0', '#ff6b6b'],
    ['#bbbe64', '#eaf0ce', '#c0c5c1', '#7d8491', '#443850', '#655a7c', '#3e442b', '#f93943', '#445e93'],
    ['#272932', '#4d7ea8', '#828489', '#9e90a2', '#b6c2d9', '#f2d0a9', '#95f2d9', '#1cfeba', '#7cdedc'],
    ['#664c43', '#873d48', '#dc758f', '#e3d3e4', '#00ffcd', '#f3f9d2', '#bdc4a7', '#92b4a7', '#55d6be'],
    ['#c9f2c7', '#aceca1', '#96be8c', '#629460', '#243119', '#fa8334', '#388697', '#271033', '#30011e'],
    ['#808d8e', '#766c7f', '#947eb0', '#a3a5c3', '#a9d2d5', '#ff5a5f', '#f3a712', '#eec584', '#122c34'],
    ['#54457f', '#ac7b84', '#4c243b', '#b84a62', '#f5a6e6', '#638475', '#90e39a', '#ddf093', '#8b9556'],
  ],[
    ['#d6f8d6', '#7fc6a4', '#5d737e', '#55505c', '#faf33e', '#3b252c', '#d6bbc0', '#d0a3bf', '#a77464', '#88292f'],
    ['#ff4d80', '#ff3e41', '#df367c', '#883955', '#4c3549', '#dde8b9', '#e8d2ae', '#acbdba', '#2e2f2f', '#051014'],
    ['#c9daea', '#03f7eb', '#00b295', '#191516', '#ab2346', '#0b5d1e', '#053b06', '#000000', '#51344d', '#6f5060'],
    ['#ca2e55', '#ffe0b5', '#8a6552', '#462521', '#bdb246', '#69a197', '#000000', '#1b2d2a', '#104547', '#6cd4ff'],
    ['#010001', '#2b0504', '#874000', '#bc5f04', '#f4442e', '#acf39d', '#9cfffa', '#e3b5a4', '#87bcde', '#cff27e'],
    ['#faa275', '#ff8c61', '#ce6a85', '#985277', '#5c374c', '#0d3b66', '#4a2545', '#000001', '#90aa86', '#461220'],
    ['#c4b7cb', '#bbc7ce', '#bfedef', '#98e2c6', '#545c52', '#2e4052', '#ffc857', '#412234', '#07004d', '#564e58'],
  ]
]

RANDOM_SETTING_ELEMENTS = [
  [
    ["default-svg-properties", {"stroke-width": 0.8, "fill": "none", "stroke-linecap": "round"}],
    ["connected-underground-belt", {"stroke": "#000001"}],
    ["connected-pipe-to-ground", {"stroke": "#000002"}]
  ],[
    ["default-svg-properties", {"stroke-width": 0.8, "fill": "none", "stroke-linecap": "round"}],
    ["connected-belt", {"stroke": "#000001"}],
    ["connected-pipe", {"stroke": "#000002"}],
    ["connected-inserter", {"stroke": "#000003"}],
    ["connected-rail", {"stroke": "#000004"}]
  ],[
    ["default-svg-properties", {"stroke": "#000005", "stroke-width": 0.2, "bbox-scale": 1, "bbox-rx": 0.15, "bbox-ry": 0.15}],
    ["bbox", {"deny": ["connected-stuff", "electric-stuff", "chests"], "bbox-scale": 1, "fill": "#000006"}],
    ["bbox", {"allow": ["electric-stuff"], "bbox-scale": 1, "fill": "#000007"}],
    ["bbox", {"allow": ["chests"], "bbox-scale": 1, "fill": "#000008"}],
    ["bbox", {"allow": ["roboport"], "bbox-scale": 1, "fill": "#000009"}],
    ["bbox", {"allow": ["beacon"], "bbox-scale": 1, "fill": "#000010"}]
  ],[
    ['default-svg-properties', {'stroke-width': 1, 'stroke': '#000011', 'fill': 'none', 'stroke-linecap': 'round'}],
    ['connected-underground-belt', {}],
    ['connected-belt', {}],
    ['connected-pipe-to-ground', {}],
    ['connected-pipe', {}]
  ],[
    ['default-svg-properties', {'stroke-width': 0.8, 'fill': 'none', 'stroke-linecap': 'round'}],
    ['bbox', {'deny': ['connected-stuff', 'electric-stuff', 'train-stuff'], 'bbox-scale': 1, 'stroke': '#000012', 'fill': '#000012', 'bbox-rx': 0.15, 'bbox-ry': 0.15}],
  ],[
    ["default-svg-properties", {"stroke-width": 1.1, "fill": "none", "stroke-linecap": "round"}],
    ['connected-underground-belt', {'stroke': '#000001'}],
    ['connected-pipe-to-ground', {'stroke': '#000002'}],
    ['connected-belt', {'stroke': '#000001'}],
    ['connected-pipe', {'stroke': '#000002'}],
    ['connected-inserter', {'stroke': '#000003'}],
    ['connected-rail', {'stroke': '#000004'}]
  ],[
    ['default-svg-properties', {'stroke': '#000013', 'stroke-width': 0.2, 'bbox-scale': 1, 'bbox-rx': 0.15, 'bbox-ry': 0.15}],
    ['bbox', {'deny': ['connected-stuff', 'electric-stuff', 'chests', 'roboport', 'beacon'], 'fill': '#000014'}],
    ['bbox', {'allow': ['electric-stuff'], 'fill': '#000015'}],
    ['bbox', {'allow': ['chests'], 'fill': '#000016'}],
    ['bbox', {'allow': ['roboport'], 'fill': '#000017'}],
    ['bbox', {'allow': ['beacon'], 'fill': '#000018'}]
  ],[
    ['default-svg-properties', {'stroke': 'none', 'stroke-width': 0, 'bbox-scale': 1, 'bbox-rx': 0.15, 'bbox-ry': 0.15}],
    ['bbox', {'allow': ['electric-stuff'], 'fill': '#000016'}],
    ['bbox', {'allow': ['chests'], 'fill': '#000017'}],
    ['bbox', {'allow': ['roboport'], 'fill': '#000018'}],
    ['bbox', {'allow': ['beacon'], 'fill': '#000019'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#000021'}],
    ['bbox', {'allow': ['lab'], 'fill': '#000022'}],
    ['bbox', {'allow': ['drill'], 'fill': '#000023'}],
    ['bbox', {'allow': ['military'], 'fill': '#000024'}],
    ['bbox', {'allow': ['connected-stuff'], 'fill': '#000020'}],
  ],[
    ['default-svg-properties', {'stroke': '#000025', 'fill': 'none', 'stroke-width': 0.2, 'bbox-scale': 0.5, 'bbox-rx': 0.15, 'bbox-ry': 0.15}],
    ['bbox', {'allow': ['electric-stuff']}],
    ['bbox', {'allow': ['chests']}],
    ['bbox', {'allow': ['roboport']}],
    ['bbox', {'allow': ['beacon']}],
    ['bbox', {'allow': ['producing-machines']}],
    ['bbox', {'allow': ['lab']}],
    ['bbox', {'allow': ['drill']}],
    ['bbox', {'allow': ['military']}],
    ['bbox', {'allow': ['connected-stuff']}],
  ],[
    ['default-svg-properties', {'stroke': '#000026', 'stroke-width': 0.2}],
    ['connected-belt', {}],
    ['connected-pipe', {}],
    ['connected-inserter', {}]
  ]
]


def settings_change_property(settings, property_name, change_func):
  settings = copy.deepcopy(settings)
  for s in settings:
    if property_name in s[1]:
      s[1][property_name] = change_func(s[1][property_name])
  return settings

def settings_change_colors(settings, color_count=None, change_background=True):
  settings = copy.deepcopy(settings)
  original_colors = {}

  keys_that_have_a_color = ["stroke", "fill"]
  if change_background:
    keys_that_have_a_color.append("background")

  for s in settings:
    for key in keys_that_have_a_color:
      if key in s[1] and s[1][key] != "none":
        if s[1][key] not in original_colors:
          original_colors[s[1][key]] = [[s[1], key]]
        else:
          original_colors[s[1][key]].append([s[1], key])
  
  original_colors_list = list(original_colors.keys())
  np.random.shuffle(original_colors_list)

  if color_count is None:
    color_count = len(original_colors_list)
  else:
    color_count = min(color_count, len(original_colors_list))
  color_count = min(10, color_count)

  color_palette = PREDEFINED_COLOR_PALETTES[color_count-2][np.random.randint(0,7)]
  np.random.shuffle(color_palette)

  for i, original_color in enumerate(original_colors_list):
    for entry, key in original_colors[original_color]:
      entry[key] = color_palette[i%len(color_palette)]
  
  return settings

def get_random_settings():
  settings = [["meta", {"background":"#000000"}]]
  num_of_entities = np.random.randint(1,4)
  for i in np.random.choice(range(len(RANDOM_SETTING_ELEMENTS)), num_of_entities, replace=False):
    num_of_rules_in_entity = np.random.randint(2,10)
    settings.extend(RANDOM_SETTING_ELEMENTS[i][:num_of_rules_in_entity])
  
  color_count = np.random.randint(2, 15)
  settings = settings_change_colors(settings, color_count, change_background=True)
  settings = settings_change_property(settings, "stroke-width", lambda v: v*np.random.uniform(0.5, 2))
  settings = settings_change_property(settings, "bbox-scale", lambda v: v*np.random.uniform(0.7, 1))
  # randomly change 'stroke-linecap' to 'round', 'square' or 'butt'
  return settings