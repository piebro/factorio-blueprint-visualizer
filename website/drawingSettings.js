const EXAMPLE_SETTINGS = [
    ["how to use: https://github.com/piebro/factorio-blueprint-visualizer/blob/master/draw_setting_documentation.md"],
    ["default settings", {'background': '#a2aebb', 'fill': 'none', 'fill-opacity': 1, 'stroke': 'none', 'stroke-linecap': 'round', 'stroke-width': 0.3, 'stroke-opacity': 1, 'scale': 0.85, 'rx': 0.1, 'ry': 0.1}],
    ["tiles", {'fill': '#420217', 'stroke': '#f3ffbd', 'stroke-width': 0.15, 'deny': [], 'scale': 0.65}],
    
    ["pipes", {'stroke': '#c84c09'}],
    ["underground-pipes", {'stroke': '#c84c09'}],
    ["belts", {'stroke': '#f3ffbd'}],
    ["underground-belts", {'stroke': '#f3ffbd'}],
    ["inserters", {'stroke': '#f3ffbd'}],
    
    ["bbox", {'fill': '#247ba0', 'deny': ["pipe", "pipe-to-ground", "belts", "inserters", "solar-panel", "accumulator", "asteroid-collector", "cargo-bay", "space-platform-hub", "thruster", "rails"]}],
    ["bbox", {'fill': '#ff1654', 'allow': ["solar-panel"]}],
    ["bbox", {'fill': '#436436', 'allow': ["accumulator"]}],
    ["bbox", {'fill': '#70c1b3', 'allow': ["cargo-bay"]}],
    ["bbox", {'fill': '#b2dbbf', 'allow': ["asteroid-collector", "thruster"]}],
    ["bbox", {'fill': '#b2dbbf', 'allow': ["space-platform-hub"], "scale": 0.95}],
    
    ["rails", {'stroke': '#b2dbbf'}],
    ["heat-pipes", {'stroke': '#b2dbbf'}],
    
]

const PREDEFINED_COLOR_PALETTES = [
    [
        ['#2d7dd2', '#97cc04'],
        ['#6d213c', '#946846'],
        ['#54457f', '#ac7b84'],
        ['#0d3b66', '#faf0ca'],
        ['#1446a0', '#db3069'],
        ['#ff6666', '#ccff66'],
        ['#251605', '#c57b57'],
        ["#353535", "#ffffff"],
        ["#34344a", "#80475e"],
        ["#e9d758", "#297373"],
        ["#c2c1c2", "#42213d"],
        ["#333745", "#e63462"],
        ["#0d3b66", "#faf0ca"],
        ["#f55d3e", "#878e88"],
        ["#fe4a49", "#2ab7ca"],
        ["#444545", "#b5ffe9"],
        ["#89b6a5", "#4c3b4d"],
        ["#f05d5e", "#0f7173"],
        ["#50514f", "#b4adea"],
      ],[
        ['#ff4e00', '#8ea604', '#f5bb00'],
        ['#a54657', '#582630', '#f7ee7f'],
        ['#464d77', '#36827f', '#f9db6d'],
        ['#264653', '#2a9d8f', '#e9c46a'],
        ['#ef767a', '#456990', '#49beaa'],
        ['#eca400', '#eaf8bf', '#006992'],
        ['#ef946c', '#c4a77d', '#70877f'],
        ["#313715", "#d16014", "#939f5c"],
        ["#442b48", "#726e60", "#98b06f"],
        ["#002a32", "#c4a29e", "#eba6a9"],
        ["#51a3a3", "#75485e", "#cb904d"],
        ["#0d3b66", "#faf0ca", "#f4d35e"],
        ["#f2c57c", "#ddae7e", "#7fb685"],
        ["#28536b", "#c2948a", "#7ea8be"],
        ["#3a2e39", "#1e555c", "#f4d8cd"],
        ["#ffa69e", "#ff7e6b", "#8c5e58"],
        ["#f4d06f", "#ff8811", "#9dd9d2"],
        ["#fbfef9", "#191923", "#0e79b2"],
        ["#bf4e30", "#c6ccb2", "#093824"],
      ],[
        ['#ec0b43', '#58355e', '#7ae7c7', '#d6ffb7'],
        ['#bfae48', '#5fad41', '#2d936c', '#391463'],
        ['#c9cba3', '#ffe1a8', '#e26d5c', '#723d46'],
        ['#d7263d', '#02182b', '#0197f6', '#448fa3'],
        ['#042a2b', '#5eb1bf', '#cdedf6', '#ef7b45'],
        ['#540d6e', '#ee4266', '#ffd23f', '#f3fcf0'],
        ['#ffb997', '#f67e7d', '#843b62', '#0b032d'],
        ["#06070e", "#29524a", "#94a187", "#c5afa0"],
        ["#f1bf98", "#e1f4cb", "#bacba9", "#717568"],
        ["#ccd7c5", "#efd2cb", "#c7a27c", "#d65780"],
        ["#ecebe4", "#cc998d", "#16f4d0", "#429ea6"],
        ["#004777", "#a30000", "#ff7700", "#efd28d"],
        ["#aba9bf", "#beb7df", "#d4f2d2", "#34113f"],
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
];

function round(num) {
  return Math.round(num * 100) / 100;
}

function randomSettings(bbox=false) {
  let svgSettings = {};
  if (bbox) {
    if (Math.random() < 0.4) {
      svgSettings['fill'] = 'color'
    };
    if (Math.random() < 0.1) {
      svgSettings['fill-opacity'] = round(Math.random() * 0.6 + 0.4);
    };
    if (Math.random() < 0.3) {
      if (Math.random() < 0.1) {
        svgSettings['scale'] = round(Math.random() * 3 + 1);
      } else {
        svgSettings['scale'] = round(Math.random());
      }
    }
    if (Math.random() < 0.2) {
      svgSettings['rx'] = Math.round(Math.random() * 100) / 100;
      svgSettings['ry'] = Math.round(Math.random() * 100) / 100;
      if (Math.random() < 0.8) {
        svgSettings['ry'] = svgSettings['rx'];
      }
    }
  }
  if (Math.random() < 0.4) {
    svgSettings['stroke'] = 'color';
  }
  if (Math.random() < 0.1) {
    if (Math.random() < 0.5) {
      svgSettings['stroke-linecap'] = 'butt';
    } else {
      svgSettings['stroke-linecap'] = 'square';
    }
  }
  if (Math.random() < 0.4) {
    svgSettings['stroke-width'] = round(Math.random());
  }
  if (Math.random() < 0.4) {
    svgSettings['stroke-opacity'] = round(Math.random() * 0.6 + 0.4);
  }
  return svgSettings;
}

function getRandomSettings() {
  let settings = [];
  settings.push(["default settings",
    {'background': 'color', 'fill': 'none', 'fill-opacity': 1, 'stroke': 'color', 'stroke-linecap': 'round', 'stroke-width': 0.3, 'stroke-opacity': 1, 'scale': 0.85, 'rx': 0.1, 'ry': 0.1},
  ]);
  
  if (Math.random() < 0.8) {
    settings.push(["tiles", {'fill': 'color', 'stroke': 'color', 'stroke-width': 0.15}, {'deny': [], 'scale': 0.7}])
  }

  const SETTING_NAMES = ["belts", "underground-belts", "pipes", "underground-pipes", "heat-pipes", "inserters", "rails", "power-lines", "green-wire-lines", "red-wire-lines"];  
  let temp_settings = [];
  
  const numSettings = Math.floor(Math.random() * 6);
  for (let i = 0; i < numSettings; i++) {
    const settingName = SETTING_NAMES[Math.floor(Math.random() * SETTING_NAMES.length)];
    const settings = randomSettings(false);
    temp_settings.push([settingName, settings]);
  }

  const bboxCount = Math.floor(Math.random() * 5);
  const genericBuildingTerms = Object.keys(buildingGenericTerms);
  const buildingTerms = Object.keys(entityNameToProperties);
  const allTerms = [...genericBuildingTerms, ...genericBuildingTerms, ...buildingTerms];
  
  for (let i = 0; i < bboxCount; i++) {
    const buildingTermCount = Math.floor(Math.random() * 5) + 1;
    const group = shuffleArray([...allTerms]).slice(0, buildingTermCount);
    const bboxGroupType = Math.random() < 0.8 ? "allow" : "deny";
    const settings = randomSettings(true);
    temp_settings.push(["bbox", {[bboxGroupType]: group, ...settings}]);
  }

  settings = [...settings, ...shuffleArray(temp_settings)];

  // Replace any "color" values with incrementing hex colors
  let noneColorCounter = 0;
  for (let s of settings) {
    if (typeof s[1] === 'object' && s[1] !== null) {
      for (let key of ['stroke', 'fill', 'background']) {
        if (key in s[1] && s[1][key] === 'color') {
          const hexColor = '#' + noneColorCounter.toString(16).padStart(6, '0');
          s[1][key] = hexColor;
          noneColorCounter++;
        }
      }
    }
  }

  return settingsChangeColors(settings, 10, true);
}

function deepCopy(obj) {
  return JSON.parse(JSON.stringify(obj));
}

function settingsChangeColors(settings, colorCount = null, changeBackground = true) {
  settings = deepCopy(settings);
  const originalColors = {};
  let keysThatHaveAColor = ["stroke", "fill"];
  if (changeBackground) {
    keysThatHaveAColor.push("background");
  }

  for (let s of settings) {
    // Only check for stroke/fill if s[1] is an object and not null
    if (typeof s[1] === 'object' && s[1] !== null) {
      for (let key of keysThatHaveAColor) {
        if (key in s[1] && s[1][key] !== "none") {
          if (!(s[1][key] in originalColors)) {
            originalColors[s[1][key]] = [[s[1], key]];
          } else {
            originalColors[s[1][key]].push([s[1], key]);
          }
        }
      }
    }
  }

  const originalColorsList = Object.keys(originalColors);
  shuffleArray(originalColorsList);

  if (colorCount === null) {
    colorCount = Math.min(10, originalColorsList.length);
  } else {
    colorCount = Math.min(colorCount, originalColorsList.length);
  }
  colorCount = Math.min(10, colorCount);

  const paletteIndex = colorCount - 2;
  const palettes = PREDEFINED_COLOR_PALETTES[paletteIndex];
  const colorPalette = [...palettes[Math.floor(Math.random() * palettes.length)]];
  shuffleArray(colorPalette);

  for (let i = 0; i < originalColorsList.length; i++) {
    const originalColor = originalColorsList[i];
    for (let [entry, key] of originalColors[originalColor]) {
      entry[key] = colorPalette[i % colorPalette.length];
    }
  }

  return settings;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}
