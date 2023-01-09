import os

def get_drawing(bbox_width, bbox_height, background_color="#dddddd", metadata_str=None, svg_width_in_mm=300, aspect_ratio=None):
  if aspect_ratio is not None:
    real_ratio = bbox_width/bbox_height
    target_ratio = aspect_ratio[0]/aspect_ratio[1]

    new_bbox_width = bbox_width
    new_bbox_height = bbox_height
    if real_ratio < target_ratio:
      new_bbox_width = target_ratio * bbox_height
      translate = [(new_bbox_width - bbox_width)/2, 0]
    else:
      new_bbox_height = 1/target_ratio * bbox_width
      translate = [0, (new_bbox_height - bbox_height)/2]

    bbox_width = new_bbox_width
    bbox_height = new_bbox_height

  dwg = {
    "groups_to_close": 0,
    "parts": [f'<svg baseProfile="tiny" height="{svg_width_in_mm*bbox_height/bbox_width}mm" version="1.2" viewBox="0,0,{bbox_width},{bbox_height}" width="{svg_width_in_mm}mm" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">']
  }

  if metadata_str is not None:
    dwg["parts"].append(metadata_str)

  if aspect_ratio is not None:
    append_group(dwg, {"transform": f"translate({translate[0]} {translate[1]})"})

  if background_color is not None:
    dwg["parts"].append(f'<rect fill="{background_color}" height="10000" width="10000" x="-100" y="-100" />')
  return dwg


def draw_lines(dwg, lines, svg_setting):
  dwg["parts"].append('<path')
  append_svg_setting(dwg, svg_setting)
  dwg["parts"].append(' d="')
  for p1, p2 in lines:
    dwg["parts"].append('M{} {} {} {}'.format(*p1, *p2))
  dwg["parts"].append('"/>')


def append_svg_setting(dwg, svg_setting, deny_list=[]):
  for key, value in svg_setting.items():
    if key not in deny_list:
      dwg["parts"].append(f' {key}="{value}"')


def append_group(dwg, svg_setting, deny_list=[]):
  dwg["parts"].append('<g')
  append_svg_setting(dwg, svg_setting, deny_list)
  dwg["parts"].append('>')
  dwg["groups_to_close"] += 1
  

def draw_rect(dwg, mid, size, scale, rx, ry):
  if scale is not None:
    size = (size[0] * scale, size[1] * scale)

  dwg["parts"].append(f'<rect height="{size[1]}" width="{size[0]}" x="{mid[0]-size[0]/2}" y="{mid[1]-size[1]/2}"')
  
  if rx is not None:
    dwg["parts"].append(f' rx="{rx}" ')
  if ry is not None:
    dwg["parts"].append(f' ry="{ry}" ')

  dwg["parts"].append('/>')


def check_for_filename(folder_path, filename, file_ending):
  if not os.path.isdir(folder_path):
    os.mkdir(folder_path)
  
  files_in_folder = os.listdir(folder_path)
  for i in range(1000):
    possible_valid_fn = f"{filename}_{i:04d}.{file_ending}"
    if possible_valid_fn not in files_in_folder:
      return os.path.join(folder_path, possible_valid_fn)


def save_svg(folder_path, filename, svg_str):
  valid_file_path = check_for_filename(folder_path, filename, "svg")
  with open(valid_file_path, "w") as text_file:
    text_file.write(svg_str)
  print("saved at:", valid_file_path)