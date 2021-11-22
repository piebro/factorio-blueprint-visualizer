import os
import json
import re

from .building_settings import BUILDING_SIZES, BUILDING_GENERIC_TERMS, ASSEMBLY_MACHINE_RESIPE_TO_DIR_CHANGE, BUILDING_PIPE_CONNECTIONS


def check_for_filename(folder_path, filename, file_ending):
  if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
  
  files_in_folder = os.listdir(folder_path)
  for i in range(10000):
    possible_valid_fn = f"{filename}_{i:05d}.{file_ending}"
    if possible_valid_fn not in files_in_folder:
      return os.path.join(folder_path, possible_valid_fn)


def save_svg(folder_path, filename, svg_str):
  valid_file_path = check_for_filename(folder_path, filename, "svg")
  with open(valid_file_path, "w") as text_file:
    text_file.write(svg_str)
  print("saved at:", valid_file_path)


def get_settings_from_svg(svg_path):
  with open(svg_path, 'r') as txt_file:
    settings_svg_str = txt_file.read()
  settings_str = re.findall(r"<settings>(.*)</settings>", settings_svg_str)[0]
  settings_str = settings_str.replace("'", "\"")
  return json.loads(settings_str)

def get_blueprint_from_svg(svg_path):
  with open(svg_path, 'r') as txt_file:
    settings_svg_str = txt_file.read()
  return re.findall(r"<blueprint>(.*)</blueprint>", settings_svg_str)[0]


def pretty_print_settings(settings):
    print("settings = " + str(settings).replace("[[", "[\n  [").replace("]]", "],\n]").replace("}], ", "}],\n  "))


def get_custom_building_settings(new_building_sizes={}, new_building_generic_terms={}, new_building_pipe_connections={}, new_recipes_in_assembly_machine_with_fluids_to_dir_change={}):
  custom_building_settings = {}
  custom_building_settings["building_sizes"] = {**BUILDING_SIZES, **new_building_sizes}
  custom_building_settings["building_generic_terms"] = {**BUILDING_GENERIC_TERMS, **new_building_generic_terms}
  custom_building_settings["building_pipe_connections"] = {**BUILDING_PIPE_CONNECTIONS, **new_building_pipe_connections}
  custom_building_settings["assembly_machine_recipe_to_dir_change"] = {**ASSEMBLY_MACHINE_RESIPE_TO_DIR_CHANGE, **new_recipes_in_assembly_machine_with_fluids_to_dir_change}
  return custom_building_settings


def replace_building_generic_terms(builing_name_list, building_generic_terms):
  new_builing_name_list = []
  for name in builing_name_list:
    if name in building_generic_terms:
      new_builing_name_list.extend(replace_building_generic_terms(building_generic_terms[name], building_generic_terms))
    else:
      new_builing_name_list.append(name)
  return new_builing_name_list