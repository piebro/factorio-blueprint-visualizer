import json
import base64
import zlib
import copy

import numpy as np

from .draw import get_drawing, draw_lines, draw_rect, append_group
from .building_settings import BUILDING_SIZES, BUILDING_GENERIC_TERMS, ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE, BUILDING_PIPE_CONNECTIONS

DIRECTION_OFFSET = np.array([[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]])


def get_blueprint_list(encoded_blueprint_str):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  blueprint_names, blueprint_jsons = [], []
  get_label_and_blueprint(blueprint_names, blueprint_jsons, raw_blueprint_json)
  return blueprint_names, blueprint_jsons


def get_label_and_blueprint(blueprint_names, blueprint_jsons, raw_blueprint_json):
  if "blueprint" in raw_blueprint_json:
    if "label" in raw_blueprint_json["blueprint"]:
      blueprint_names.append(raw_blueprint_json['blueprint']['label'])
    else:
      blueprint_names.append("")
    blueprint_jsons.append(raw_blueprint_json["blueprint"])

  elif "blueprint_book" in raw_blueprint_json:
    for raw_blueprint in raw_blueprint_json["blueprint_book"]["blueprints"]:
      get_label_and_blueprint(blueprint_names, blueprint_jsons, raw_blueprint)


def get_blueprint(blueprint_json, bbox_border_NWSE=[3,3,3,3]):
  blueprint_json_str = json.dumps({'blueprint': blueprint_json}, separators=[",",":"], ensure_ascii=False).encode('utf8')
  encoded_blueprint_str = base64.b64encode(zlib.compress(blueprint_json_str, level=9)).decode()
  entities = get_simplified_entities(blueprint_json)
  bbox_width, bbox_height = get_size_and_normalize_entities(entities, bbox_border_NWSE=bbox_border_NWSE)
  return {
    "entities": entities,
    "bbox_width": bbox_width,
    "bbox_height": bbox_height,
    "encoded_blueprint_str": encoded_blueprint_str,
    "cache": {},
  }


def get_simplified_entities(blueprint_json):
  blueprint_json = copy.deepcopy(blueprint_json)
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


def get_size_and_normalize_entities(entities, bbox_border_NWSE):
  if len(entities) == 0:
    return 1, 1
  entity_bboxes = []
  for e in entities:
    if e["name"] in BUILDING_SIZES:
      if e["direction"]%2 == 0:
        size_x, size_y = BUILDING_SIZES[e["name"]]
      else:
        size_y, size_x = BUILDING_SIZES[e["name"]]
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


def draw_blueprint(blueprint, settings, svg_width_in_mm=300, aspect_ratio=None):
  metadata_str = str(settings)
  metadata_str = f'<metadata generated_with="https://piebro.github.io/factorio-blueprint-visualizer"><settings>{settings}</settings><blueprint>{blueprint["encoded_blueprint_str"]}</blueprint></metadata>'

  settings = pre_process_settings(settings)
  background = settings[0][1]

  default_bbox_prop = {"scale": None, "rx": None, "ry": None}
  
  dwg = get_drawing(blueprint["bbox_width"], blueprint["bbox_height"], background, metadata_str, svg_width_in_mm, aspect_ratio)
  
  for setting_name, setting_options in settings:
    if setting_name == "background":
      continue

    elif setting_name == "svg":
      append_group(dwg, setting_options, deny_list=["bbox-scale", "bbox-rx", "bbox-ry"])
      for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
        if bbox_prop_key in setting_options:
          default_bbox_prop[bbox_prop_key[5:]] = setting_options[bbox_prop_key]
      
    elif setting_name == "bbox":
      draw_entities_bbox(dwg, blueprint["entities"], setting_options, default_bbox_prop)
      
    elif setting_name == "belts":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_belt(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    elif setting_name == "underground-belts":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_underground_belt(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)
    
    elif setting_name == "pipes":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_pipes(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    elif setting_name == "underground-pipes":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_underground_pipes(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)
  
    elif setting_name == "inserters":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_inserter(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    elif setting_name == "rails":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_rails(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)
    
    elif setting_name == "electricity":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_electricity(blueprint["entities"])
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    elif setting_name == "red-circuits":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_circuit(blueprint["entities"], "red")
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    elif setting_name == "green-circuits":
      if setting_name not in blueprint["cache"]:
        blueprint["cache"][setting_name] = get_lines_circuit(blueprint["entities"], "green")
      draw_lines(dwg, blueprint["cache"][setting_name], setting_options)

    else:
      print("unknown setting name:", setting_name)

  for _ in range(dwg["groups_to_close"]):
    dwg["parts"].append('</g>')
  dwg["parts"].append("</svg>")
  return "".join(dwg["parts"])


def pre_process_settings(settings):
  settings = copy.deepcopy(settings)
  if settings[0][0] != "background":
    settings = [("background", "#E6E6E6"), *settings]
  
  for setting_name, setting_options in settings:
    if setting_name == "bbox":
      if "allow" in setting_options:
        setting_options["allow"] = resolve_building_gerneric_names(setting_options["allow"])
      elif "deny" in setting_options:
        setting_options["deny"] = resolve_building_gerneric_names(setting_options["deny"])

  return settings


def resolve_building_gerneric_names(build_name_list):
  builing_name_list_without_generic_terms = []
  for name in build_name_list:
    if name in BUILDING_GENERIC_TERMS:
      builing_name_list_without_generic_terms.extend(BUILDING_GENERIC_TERMS[name])
    else:
      builing_name_list_without_generic_terms.append(name)
  return builing_name_list_without_generic_terms


def draw_entities_bbox(dwg, entities, settings, default_bbox_prop):
  if "allow" in settings:
    bbox_entities = [e for e in entities if e["name"] in settings["allow"]]
  elif "deny" in settings:
    bbox_entities = [e for e in entities if e["name"] not in settings["deny"]]
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
    if e["name"] in BUILDING_SIZES:
      if e["direction"]%4 == 0:
        size_x, size_y = BUILDING_SIZES[e["name"]]
      else:
        size_y, size_x = BUILDING_SIZES[e["name"]]
      draw_rect(dwg, e["pos"], (size_x, size_y), **bbox_prop)
  dwg["groups_to_close"] -= 1
  dwg["parts"].append('</g>')


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


def get_lines_pipes(entities):
  nodes = {}
  connect_conditions = []
  for e in entities:
    if e["name"] not in BUILDING_PIPE_CONNECTIONS:
      continue
      
    if e["name"] in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
      if "recipe" not in e:
        continue

      if e["recipe"] in ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE:
        recipe_dir_change = ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE[e["recipe"]]
      else:
        continue
    else:
      recipe_dir_change = 0

    for connection in BUILDING_PIPE_CONNECTIONS[e["name"]]:
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
