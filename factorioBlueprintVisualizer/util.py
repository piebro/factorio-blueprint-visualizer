import re
import json

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
    print("settings = " + str(settings).replace("[[", "[\n  [").replace("]]", "],\n]").replace("}], ", "}],\n  ").replace("], [", "],\n  ["))