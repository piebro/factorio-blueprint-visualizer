import copy
import numpy as np

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
    ['default-svg-properties', {'stroke-width': 1, 'stroke': '#000011', 'fill': 'none', 'stroke-linecap': 'round'}],
    ['connected-underground-belt', {'stroke-opacity': 0.7}],
    ['connected-belt', {}],
    ['connected-pipe-to-ground', {'stroke-opacity': 0.7}],
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
    ['default-svg-properties', {'stroke': 'none', 'stroke-width': 0, 'bbox-scale': 1, 'bbox-rx': 0.15, 'bbox-ry': 0.15, "stroke-linecap": "round"}],
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
    ['default-svg-properties', {'stroke': '#000026', 'stroke-width': 0.2, "stroke-linecap": "round"}],
    ['connected-belt', {}],
    ['connected-pipe', {}],
    ['connected-inserter', {}]
  ],[
    ['default-svg-properties', {'stroke': '#000027', 'stroke-width': 0.2, "stroke-linecap": "round"}],
    ['connected-belt', {}],
    ['connected-pipe', {}],
    ['connected-rail', {}]
  ],[
    ['default-svg-properties', {'stroke': '#000028', 'stroke-width': 0.3, 'fill': 'none', 'bbox-scale': 1, 'bbox-rx': 0.15, 'bbox-ry': 0.15}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#000029'}],
    ['bbox', {'allow': ['roboport'], 'fill': '#000030'}],
    ['bbox', {'allow': ['lab'], 'fill': '#000031'}],
    ['bbox', {'allow': ['beacon'], 'fill': '#000032'}],
    ['bbox', {'allow': ['electicity-generation', 'boiler'], 'fill': '#000033'}],
    ['bbox', {'allow': ['drill'], 'fill': '#000034'}],
    ['bbox', {'allow': ['furnace'], 'fill': '#000035'}]
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
    num_of_rules_in_entity = np.random.randint(2,12)
    c = RANDOM_SETTING_ELEMENTS[i][1:].copy()
    np.random.shuffle(c)
    random_setting_elements = [RANDOM_SETTING_ELEMENTS[i][0], *c]
    settings.extend(random_setting_elements[:num_of_rules_in_entity])
  
  color_count = np.random.randint(2, 15)

  uniform_stroke = np.random.uniform(1)<0.3
  if uniform_stroke:
    settings = settings_change_property(settings, "stroke", lambda v: "#000100")

  settings = settings_change_colors(settings, color_count, change_background=True)
  
  if uniform_stroke:
    settings = settings_change_property(settings, "stroke-width", lambda v: "#000100")
  else:
    settings = settings_change_property(settings, "stroke-width", lambda v: v*np.random.uniform(0.5, 2))
  
  settings = settings_change_property(settings, "bbox-scale", lambda v: v*np.random.uniform(0.7, 1))
  settings = settings_change_property(settings, "stroke-linecap", lambda v: v if np.random.uniform(1)<0.8 else np.random.choice(["butt", "round", "square"]))
  
  return settings