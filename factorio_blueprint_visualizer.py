import json
import zlib
import base64
import random
import os
import re

import numpy as np

from building_settings import BUILDING_SIZES, BUILDING_GENERIC_TERMS, RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE, BUILDING_PIPE_CONNECTIONS

from draw import get_drawing, draw_lines, draw_rect, append_group

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


def get_blueprint_cache(encoded_blueprint_str, blueprint_name_or_number, bbox_border=3, custom_building_settings={}):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  
  building_sizes = custom_building_settings["BUILDING_SIZES"] if "BUILDING_SIZES" in custom_building_settings else BUILDING_SIZES

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