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