import json
import base64
import zlib
import random

import numpy as np

from .draw import get_drawing, draw_lines, draw_rect, append_group
from .util import replace_building_generic_terms, get_custom_building_settings
from .building_settings import BUILDING_SIZES

DIRECTION_OFFSET = np.array([[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]])


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


def get_size_and_normalize_entities(entities, bbox_border_NWSE, building_sizes):
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
  bbox += np.array([-bbox_border_NWSE[1], -bbox_border_NWSE[0], bbox_border_NWSE[3], bbox_border_NWSE[2]])
  bbox_width = bbox[2]-bbox[0] 
  bbox_height = bbox[3]-bbox[1]

  for e in entities:
    if "pos" in e:
      e["pos"] -= bbox[:2]

  return bbox_width, bbox_height


def get_blueprint_cache(encoded_blueprint_str, blueprint_name_or_number=0, bbox_border_NWSE=[3,3,3,3], building_settings=None):
  if building_settings is None:
    building_settings = get_custom_building_settings()

  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))

  blueprint_dict = {}
  get_label_and_blueprint(blueprint_dict, raw_blueprint_json)

  if isinstance(blueprint_name_or_number, str):
    blueprint_name = blueprint_name_or_number
  else:
    blueprint_name = list(blueprint_dict.keys())[blueprint_name_or_number]

  blueprint_json_str = json.dumps({'blueprint': blueprint_dict[blueprint_name]}, separators=[",",":"], ensure_ascii=False).encode('utf8')
  encoded_selected_blueprint_str = encoded_blueprint_str[0] + base64.b64encode(zlib.compress(blueprint_json_str, level=9)).decode()
  
  entities = get_simplified_entities(blueprint_dict[blueprint_name])
  bbox_width, bbox_height = get_size_and_normalize_entities(entities, bbox_border_NWSE, building_settings["building_sizes"])

  cache = {
    "bbox_width": bbox_width,
    "bbox_height": bbox_height,
    "entities": entities,
    "encoded_blueprint": encoded_selected_blueprint_str,
    "building_settings": building_settings
  }
  return cache


def draw_entities_bbox(dwg, entities, settings, default_bbox_prop, building_settings):
  if "allow" in settings:
    allow_resolved_generic_terms = replace_building_generic_terms(settings["allow"], building_settings["building_generic_terms"])
    bbox_entities = [e for e in entities if e["name"] in allow_resolved_generic_terms]
  elif "deny" in settings:
    deny_resolved_generic_terms = replace_building_generic_terms(settings["deny"], building_settings["building_generic_terms"])
    bbox_entities = [e for e in entities if e["name"] not in deny_resolved_generic_terms]
  else:
    bbox_entities = entities
    
  bbox_prop = {}
  for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
    if bbox_prop_key in settings:
      bbox_prop[bbox_prop_key[5:]] = settings[bbox_prop_key]
    else:
      bbox_prop[bbox_prop_key[5:]] = default_bbox_prop[bbox_prop_key[5:]]

  append_group(dwg, settings, deny_list=["bbox-scale", "bbox-rx", "bbox-ry", "allow", "deny"])
  for e in bbox_entities:
    if e["name"] in building_settings["building_sizes"]:
      if e["direction"]%4 == 0:
        size_x, size_y = building_settings["building_sizes"][e["name"]]
      else:
        size_y, size_x = building_settings["building_sizes"][e["name"]]
      draw_rect(dwg, e["pos"], (size_x, size_y), **bbox_prop)
  dwg.append('</g>')


def add_pos_to_nodes(nodes, pos, dir):
  if pos not in nodes:
    nodes[pos] = [False, False, False, False, False, False, False, False]
  nodes[pos][dir] = True


def rotate(angle, pos):
  if angle==0:
    return pos
  elif angle==2:
    return (-pos[1], pos[0])
  elif angle==4:
    return (-pos[0], -pos[1])
  elif angle==6:
    return (pos[1], -pos[0])


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


def get_lines_inserter(entities):
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


def get_lines_pipes(entities, building_settings):
  nodes = {}
  connect_conditions = []
  for e in entities:
    if e["name"] not in building_settings["building_pipe_connections"]:
      continue
      
    if e["name"] in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
      if "recipe" not in e:
        continue

      if e["recipe"] in building_settings["assembly_machine_recipe_to_dir_change"]:
        recipe_dir_change = building_settings["assembly_machine_recipe_to_dir_change"][e["recipe"]]
      else:
        continue
    else:
      recipe_dir_change = 0

    for connection in building_settings["building_pipe_connections"][e["name"]]:
      pos = tuple(e["pos"] + rotate((e["direction"] + recipe_dir_change)%8, connection["pos"]))
      dir = (e["direction"] + connection["direction"] + recipe_dir_change)%8
      add_pos_to_nodes(nodes, tuple(pos), dir)

      target_pos = tuple(np.array(pos) + DIRECTION_OFFSET[dir])
      target_dir = (dir+4)%8
      connect_conditions.append([pos, dir, target_pos, target_dir])

  return get_lines_nodes_and_connect_conditions(nodes, connect_conditions)


def get_lines_underground_pipes(entities, max_length=11):
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


def get_lines_belt(entities):
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
        
  lines = get_lines_nodes_and_connect_conditions(nodes, connect_conditions, draw_nodes=False, set_self_false=False, set_target_false=False)

  for e in entities:
    if e["name"] in ["splitter", "fast-splitter", "express-splitter"]:
      dir = e["direction"]
      offset = 0.5*DIRECTION_OFFSET[(dir+2)%8]
      pos_1_2 = [tuple(e["pos"]-offset), tuple(e["pos"]+offset)]
      from_pos_1_2 = [tuple(np.array(pos) - DIRECTION_OFFSET[dir]) for pos in pos_1_2]
      to_pos_1_2 = [tuple(np.array(pos) + DIRECTION_OFFSET[dir]) for pos in pos_1_2]
      
      to_pos_in_nodes = [to_pos_1_2[i] in nodes and not nodes[to_pos_1_2[i]][dir-4] for i in [0,1]]
      from_pos_in_nodes = [from_pos_1_2[i] in nodes and nodes[from_pos_1_2[i]][dir] for i in [0,1]]

      for i in [0,1]:
        if to_pos_in_nodes[i] and (not from_pos_in_nodes[i-1] or from_pos_in_nodes[i]):
          lines.append([pos_1_2[i], to_pos_1_2[i]])
        
        if from_pos_in_nodes[i]:
          lines.append([from_pos_1_2[i], pos_1_2[i]])
        
          if to_pos_in_nodes[i-1]:
            lines.append([pos_1_2[i], to_pos_1_2[i-1]])

  return lines



def get_lines_underground_belt(entities, entity_name=None, max_length=None):
  if entity_name is None and max_length is None:
    lines = get_lines_underground_belt(entities, "underground-belt", 6)
    lines.extend(get_lines_underground_belt(entities, "fast-underground-belt", 8))
    lines.extend(get_lines_underground_belt(entities, "express-underground-belt", 10))
    return lines

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


def get_lines_rails(entities):
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


def get_lines_circuit(entities, circuit_color):
    lines = []
    for e in entities:
        if "connections" in e:
            connected_entity_ids = []
            if "1" in e["connections"] and circuit_color in e["connections"]["1"]:
                connected_entity_ids.extend([i["entity_id"] for i in e["connections"]["1"][circuit_color]])
            if "2" in e["connections"] and circuit_color in e["connections"]["2"]:
                connected_entity_ids.extend([i["entity_id"] for i in e["connections"]["2"][circuit_color]])
            lines.extend([[e["pos"], entities[n-1]["pos"]] for n in connected_entity_ids])
    return lines


def get_lines_electricity(entities):
    lines = []
    for e in entities:
        if "neighbours" in e:
          lines.extend([[e["pos"], entities[n-1]["pos"]] for n in e["neighbours"]])

    return lines


def draw_blueprint(blueprint_cache, settings, svg_max_size_in_mm=300):
  meta_settings = settings[0][1] if settings[0][0] == "meta" else {"background":"#E6E6E6"}
  
  entities = blueprint_cache["entities"]

  metadata_str = f'<metadata generated_with="https://piebro.github.io/factorio-blueprint-visualizer"><settings>{settings}</settings><blueprint>{blueprint_cache["encoded_blueprint"]}</blueprint></metadata>'

  dwg = get_drawing(blueprint_cache["bbox_width"], blueprint_cache["bbox_height"], svg_max_size_in_mm, meta_settings["background"], metadata_str)  
  
  dwg_groups_to_close = 0
  default_bbox_prop = {"scale": None, "rx": None, "ry": None}
  
  for setting_name, setting_options in settings:
    if setting_name == "meta":
      continue

    elif setting_name == "svg":
      append_group(dwg, setting_options, deny_list=["bbox-scale", "bbox-rx", "bbox-ry"])
      dwg_groups_to_close += 1
      for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
        if bbox_prop_key in setting_options:
          default_bbox_prop[bbox_prop_key[5:]] = setting_options[bbox_prop_key]
      
    elif setting_name == "bbox":
      draw_entities_bbox(dwg, entities, setting_options, default_bbox_prop, blueprint_cache["building_settings"])
      
    elif setting_name == "belts":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_belt(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    elif setting_name == "underground-belts":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_underground_belt(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)
    
    elif setting_name == "pipes":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_pipes(entities, blueprint_cache["building_settings"])
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    elif setting_name == "underground-pipes":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_underground_pipes(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)
  
    elif setting_name == "inserters":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_inserter(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    elif setting_name == "rails":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_rails(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)
    
    elif setting_name == "electricity":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_electricity(entities)
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    elif setting_name == "red-circuits":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_circuit(entities, "red")
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    elif setting_name == "green-circuits":
      if setting_name not in blueprint_cache:
        blueprint_cache[setting_name] = get_lines_circuit(entities, "green")
      draw_lines(dwg, blueprint_cache[setting_name], setting_options)

    else:
      print("unknown setting name:", setting_name)

  for _ in range(dwg_groups_to_close):
    dwg.append('</g>')
  dwg.append("</svg>")
  return "".join(dwg)



