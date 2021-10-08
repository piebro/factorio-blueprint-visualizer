import json
import zlib
import base64
import copy
import random
import os

import numpy as np

from building_settings import BUILDING_SIZES, BUILDING_GENERIC_TERMS, RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE, BUILDING_PIPE_CONNECTIONS

from draw import get_drawing, draw_lines, draw_rect, append_group

DIRECTION_OFFSET = np.array([[0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1]])

# generated with: https://coolors.co/
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

def get_size_and_normalize_entities(entities, bbox_border=3):
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

def get_lines_pipes(dwg, entities):
  nodes = {}
  connect_conditions = []
  for e in entities:
    if e["name"] not in BUILDING_PIPE_CONNECTIONS:
      continue
      
    if e["name"] in ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"]:
      if "recipe" not in e:
        continue

      if e["recipe"] in RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE:
        recipe_dir_change = RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE[e["recipe"]]
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


def replace_building_generic_terms(builing_name_list):
  new_builing_name_list = []
  for name in builing_name_list:
    if name in BUILDING_GENERIC_TERMS:
      new_builing_name_list.extend(BUILDING_GENERIC_TERMS[name])
    else:
      new_builing_name_list.append(name)
  return new_builing_name_list

def draw_entities_bbox(dwg, entities, settings, default_bbox_prop):

  if "allow" in settings:
    bbox_entities = [e for e in entities if e["name"] in replace_building_generic_terms(settings["allow"])]
  elif "deny" in settings:
    bbox_entities = [e for e in entities if e["name"] not in replace_building_generic_terms(settings["deny"])]
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
    if e["name"] in BUILDING_SIZES:
      if e["direction"]%4 == 0:
        size_x, size_y = BUILDING_SIZES[e["name"]]
      else:
        size_y, size_x = BUILDING_SIZES[e["name"]]
      draw_rect(dwg, e["pos"], (size_x, size_y), **bbox_prop)
  dwg.append('</g>')

def get_blueprint_labels(encoded_blueprint_str):
  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  blueprint_dict = {}
  get_label_and_blueprint(blueprint_dict, raw_blueprint_json)
  return list(blueprint_dict.keys())

def draw_blueprints(encoded_blueprint_str, blueprint_name_or_number, settings):

  raw_blueprint_json = json.loads(zlib.decompress(base64.b64decode(encoded_blueprint_str[1:])))
  
  blueprint_dict = {}
  get_label_and_blueprint(blueprint_dict, raw_blueprint_json)
  
  if isinstance(blueprint_name_or_number, str):
    blueprint_name = blueprint_name_or_number
  else:
    blueprint_name = list(blueprint_dict.keys())[blueprint_name_or_number]

  default_meta_settings = {"background":"#E6E6E6", "bbox_border":3, "max_size_in_mm": 300}
  if settings[0][0] == "meta":
    meta_settings = {**default_meta_settings, **settings[0][1]}
  else:
    meta_settings = default_meta_settings

  entities = get_simplified_entities(blueprint_dict[blueprint_name])
  bbox_width, bbox_height = get_size_and_normalize_entities(entities, meta_settings["bbox_border"])
  dwg = get_drawing(bbox_width, bbox_height, meta_settings["max_size_in_mm"], meta_settings["background"])
  
  dwg_groups_to_close = 0
  default_bbox_prop = {"scale": None, "rx": None, "ry": None}
  
  cache = {}
  for setting in settings:
    if setting[0] == "default-svg-properties":
      append_group(dwg, setting[1], deny_list=["bbox-scale", "bbox-rx", "bbox-ry"])
      dwg_groups_to_close += 1
      for bbox_prop_key in ["bbox-scale", "bbox-rx", "bbox-ry"]:
        if bbox_prop_key in setting[1]:
          default_bbox_prop[bbox_prop_key[5:]] = setting[1][bbox_prop_key]
      
    elif setting[0] == "bbox":
      draw_entities_bbox(dwg, entities, setting[1], default_bbox_prop)
      
    elif setting[0] == "connected-belt":
      if "connected-belt" not in cache:
        cache["connected-belt"] = get_lines_belt(dwg, entities)
      draw_lines(dwg, cache["connected-belt"], setting[1])

    elif setting[0] == "connected-underground-belt":
      if "connected-underground-belt" not in cache:
        lines = get_lines_underground_belt(dwg, entities, "underground-belt", 6)
        lines.extend(get_lines_underground_belt(dwg, entities, "fast-underground-belt", 8))
        lines.extend(get_lines_underground_belt(dwg, entities, "express-underground-belt", 10))
        cache["connected-underground-belt"] = lines
      draw_lines(dwg, cache["connected-underground-belt"], setting[1])

    elif setting[0] == "connected-pipe-to-ground":
      if "connected-pipe-to-ground" not in cache:
        cache["connected-pipe-to-ground"] = get_lines_underground_pipes(dwg, entities, 11)
      draw_lines(dwg, cache["connected-pipe-to-ground"], setting[1])

    elif setting[0] == "connected-pipe":
      if "connected-pipe" not in cache:
        cache["connected-pipe"] = get_lines_pipes(dwg, entities)
      draw_lines(dwg, cache["connected-pipe"], setting[1])
  
    elif setting[0] == "connected-inserter":
      if "connected-inserter" not in cache:
        cache["connected-inserter"] = get_lines_inserter(dwg, entities)
      draw_lines(dwg, cache["connected-inserter"], setting[1])

    elif setting[0] == "connected-rail":
      if "connected-rail" not in cache:
        cache["connected-rail"] = get_lines_rails(dwg, entities)
      draw_lines(dwg, cache["connected-rail"], setting[1])

  for _ in range(dwg_groups_to_close):
    dwg.append('</g>')
  dwg.append("</svg>")
  return "".join(dwg)


def change_colors_in_settings(settings, color_count=None, change_background=True):
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
    color_count = np.random.randint(2, min(10, max(3,len(original_colors_list))))

  color_palette = PREDEFINED_COLOR_PALETTES[color_count-2][np.random.randint(0,7)]
  np.random.shuffle(color_palette)

  for i, original_color in enumerate(original_colors_list):
    for entry, key in original_colors[original_color]:
      entry[key] = color_palette[i%len(color_palette)]
  
  return settings

def save_svg_and_settings(folder_path, svg_str, settings):
  files_in_folder = os.listdir(folder_path)
  for i in range(1000):
    save_name_svg = f"save_{i:04d}.svg"
    save_name_json = f"save_{i:04d}.json"
    if save_name_svg not in files_in_folder and save_name_json not in files_in_folder:

      
      with open(os.path.join(folder_path, save_name_svg), "w") as text_file:
        text_file.write(svg_str)
      with open(os.path.join(folder_path, save_name_json), "w") as text_file:
        text_file.write(json.dumps(settings, indent=2))

      print("saved to:", save_name_svg, "and", save_name_json)
      return