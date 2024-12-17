const EXAMPLE_SETTINGS = [
    ['background', '#a2aebb'],
    ['svg', {'stroke': '#3f88c5', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
    ['tiles', {'fill': '#a2aefb', 'stroke-width': 1}],
    ['bbox', {'bbox-scale': 1, 'deny': ["labs"], 'fill': 'none', 'stroke': '#ffba08'}],
    
    ['pipes', {'stroke-opacity': 0.8}],
    ['underground-pipes'],
    ['belts'],
    ['underground-belts'],

    ['heat-pipes', {'stroke-opacity': 0.8}],
    ['power-lines', {'stroke-opacity': 0.8}],
    ['green-wire-lines', {'stroke-opacity': 0.8, 'stroke': '#00ff08'}],
    ['red-wire-lines', {'stroke-opacity': 0.8, 'stroke': '#ff0008'}],
    ['inserters', {}],
    
    // ['bbox', {'bbox-scale': 1, 'allow': ['transportation'], 'fill': 'none', 'stroke': '#ffba08', 'stroke-width': 0.1}],
    // ['belts', {'stroke': '#3f88c5', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
    // ['rails', {'stroke': '#3f88c5', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
    // ['underground-belts', {'stroke-opacity': 0.6}],
    
    // ['underground-pipes', {'stroke-opacity': 0.6}],
    
    
    // ['bbox', {'allow': ['furnaces', 'electricity-generators', 'boiler'], 'fill': '#1c3144', 'stroke': 'none'}],
    // ['bbox', {'allow': ['lab'], 'fill': '#1c3144', 'stroke': 'none'}],
    // ['bbox', {'deny': ['transportation', 'electricity', 'inserters'], 'fill': 'none'}],
];

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

const RANDOM_SETTING_LIST = [
  [
    ['background', '#cfd186'],
    ['svg', {'fill': 'none', 'stroke': '#596157', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#5b8c5a', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#52414c', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#e3655b', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#e3655b', 'stroke': 'none'}],
    ['bbox', {'allow': ['military'], 'fill': '#d67ab1', 'stroke': 'none'}],
    ['bbox', {'deny': ['transportation', 'electricity', 'inserters', 'electricity-generators', 'boiler']}],
  ],[
    ['background', '#faf0ca'],
    ['svg', {'fill': 'none', 'stroke': '#0d3b66', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
    ['belts', {}],
    ['bbox', {'deny': ['belts']}],
    ['electricity', {}],
  ],[
    ['background', '#5998c5'],
    ['svg', {'bbox-scale': 0.7, 'stroke': '#12eaea', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#8eb1c7', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#fff689', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#e03616', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#cfffb0', 'stroke': 'none'}],
    ['bbox', {'allow': ['military'], 'fill': '#58355e', 'stroke': 'none'}],
  ],[
    ['background', '#36827f'],
    ['bbox', {'bbox-scale': 0.85, 'deny': ['transportation', 'electricity', 'inserters'], 'fill': '#f9db6d', 'stroke': 'none'}],
    ['electricity', {'stroke': '#f9db6d', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
  ],[
    ['background', '#58355e'],
    ['svg', {'bbox-scale': 0.7, 'fill': 'none', 'stroke': '#cfffb0', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#e03616', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#8eb1c7', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#5998c5', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#fff689', 'stroke': 'none'}],
    ['bbox', {'allow': ['military'], 'fill': '#12eaea', 'stroke': 'none'}],
  ],[
    ['background', '#eddea4'],
    ['svg', {'fill': 'none', 'stroke': '#f7a072', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#e08dac', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#0fa3b1', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#ff9b42', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#ff9b42', 'stroke': 'none'}],
    ['bbox', {'allow': ['military'], 'fill': '#d9e5d6', 'stroke': 'none'}],
    ['bbox', {'deny': ['transportation', 'electricity', 'inserters', 'electricity-generators', 'boiler']}],
  ],[
    ['background', '#a2aebb'],
    ['svg', {'stroke': '#3f88c5', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['pipes', {}],
    ['underground-pipes', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#ffba08', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#d00000', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces', 'electricity-generators', 'boiler'], 'fill': '#1c3144', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#1c3144', 'stroke': 'none'}],
    ['bbox', {'deny': ['transportation', 'electricity', 'inserters'], 'fill': 'none'}],
  ],[
    ['background', '#2a9d8f'],
    ['svg', {'bbox-scale': 0.85, 'stroke': '#e9c46a', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#264653', 'stroke': 'none'}],
  ],[
    ['background', '#6cd4ff'],
    ['svg', {'bbox-scale': 0.65, 'stroke': '#1b2d2a', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['rails', {}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#8a6552', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#462521', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#bdb246', 'stroke': 'none'}],
    ['bbox', {'allow': ['inserters'], 'fill': '#ffe0b5', 'stroke': 'none'}],
    ['bbox', {'allow': ['beacon'], 'fill': '#69a197', 'stroke': 'none'}],
    ['bbox', {'allow': ['electricity'], 'fill': '#104547', 'stroke': 'none'}],
    ['bbox', {'allow': ['roboport'], 'fill': '#ca2e55', 'stroke': 'none'}],
    ['bbox', {'allow': ['chests'], 'fill': '#000000', 'stroke': 'none'}],
  ],[
    ['background', '#52414c'],
    ['svg', {'bbox-scale': 0.9, 'stroke': '#e3655b', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['pipes', {'stroke': '#596157'}],
    ['underground-pipes', {'stroke': '#596157', 'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#5b8c5a', 'stroke': 'none'}],
    ['bbox', {'allow': ['beacon'], 'fill': '#cfd186', 'stroke': 'none'}],
    ['bbox', {'allow': ['electricity'], 'fill': '#d67ab1', 'stroke': 'none'}],
  ],[
    ['background', '#006494'],
    ['svg', {'bbox-scale': 0.9, 'stroke': '#13293d', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#5d675b', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#f78e69', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#f7ef99', 'stroke': 'none'}],
    ['bbox', {'allow': ['electricity'], 'fill': '#f1bb87', 'stroke': 'none'}],
  ],[
    ['background', '#52489c'],
    ['svg', {'bbox-scale': 0.9, 'stroke': '#f45b69', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['drills'], 'fill': '#4062bb', 'stroke': 'none'}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#ebebeb', 'stroke': 'none'}],
    ['bbox', {'allow': ['furnaces'], 'fill': '#59c3c3', 'stroke': 'none'}],
  ],[
    ['background', '#ffba08'],
    ['svg', {'bbox-scale': 0.9, 'fill': 'none', 'stroke': '#3f88c5', 'stroke-linecap': 'round', 'stroke-width': 0.25}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.6}],
    ['bbox', {'allow': ['producing-machines'], 'fill': '#1c3144', 'stroke': 'none'}],
    ['bbox', {'allow': ['lab'], 'fill': '#a2aebb', 'stroke': 'none'}],
    ['bbox', {'allow': ['electricity'], 'fill': '#d00000', 'stroke': 'none'}],
  ],[
    ['background', '#353535'],
    ['svg', {'stroke': '#ffffff', 'stroke-linecap': 'round', 'stroke-width': 0.2}],
    ['belts', {}],
    ['underground-belts', {'stroke-opacity': 0.7}],
    ['bbox', {'deny': ['belts'], 'fill': 'none'}],
    ['electricity', {}],
  ],[
    ['background', '#444545'],
    ['electricity', {'stroke': '#b5ffe9', 'stroke-linecap': 'round', 'stroke-width': 0.4}],
  ]
];

function deepCopy(obj) {
  return JSON.parse(JSON.stringify(obj));
}

function settingsChangeProperty(settings, propertyName, changeFunc) {
  settings = deepCopy(settings);
  for (let s of settings) {
    // Only check properties if s[1] is an object
    if (typeof s[1] === 'object' && s[1] !== null && propertyName in s[1]) {
      s[1][propertyName] = changeFunc(s[1][propertyName]);
    }
  }
  return settings;
}

function settingsChangeColors(settings, colorCount = null, changeBackground = true) {
  settings = deepCopy(settings);
  const originalColors = {};
  const keysThatHaveAColor = ["stroke", "fill"];

  for (let s of settings) {
    // Handle background color
    if (changeBackground && s[0] === "background") {
      if (!(s[1] in originalColors)) {
        originalColors[s[1]] = [[s, 1]];
      } else {
        originalColors[s[1]].push([s, 1]);
      }
      continue;
    }

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

function getRandomSettings() {
  let settings = deepCopy(RANDOM_SETTING_LIST[Math.floor(Math.random() * RANDOM_SETTING_LIST.length)]);

  if (Math.random() < 0.4) {
    const additionalSettings = RANDOM_SETTING_LIST[Math.floor(Math.random() * RANDOM_SETTING_LIST.length)];
    settings = [...settings, ...additionalSettings];
    settings = settingsChangeColors(settings);
  }

  if (Math.random() < 0.3) {
    const additionalSettings = RANDOM_SETTING_LIST[Math.floor(Math.random() * RANDOM_SETTING_LIST.length)];
    settings = [...settings, ...additionalSettings];
    if (settings.length > 8) {
      const indices = [0, 1, ...shuffleArray([...Array(settings.length).keys()].slice(2)).slice(0, settings.length - 4)];
      settings = settings.filter((_, i) => indices.includes(i));
    }
    settings = settingsChangeColors(settings);
  }

  if (Math.random() < 0.8) {
    settings = settingsChangeColors(settings, Math.floor(Math.random() * 10) + 2);
  }

  if (Math.random() < 0.5) {
    settings = settingsChangeProperty(settings, "stroke-width", v => v * (Math.random() * 1.5 + 0.5));
  }

  if (Math.random() < 0.5) {
    settings = settingsChangeProperty(settings, "bbox-scale", v => v * (Math.random() * 0.3 + 0.7));
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

function preProcessSettings(settings) {
  settings = JSON.parse(JSON.stringify(settings)); // Deep copy
  if (settings[0][0] !== "background") {
      settings.unshift(["background", "#E6E6E6"]);
  }

  for (const [settingName, settingOptions] of settings) {
      if (settingName === "bbox") {
          if ("allow" in settingOptions) {
              settingOptions.allow = resolveBuildingGenericNames(settingOptions.allow);
          } else if ("deny" in settingOptions) {
              settingOptions.deny = resolveBuildingGenericNames(settingOptions.deny);
          }
      }
  }

  return settings;
}

function resolveBuildingGenericNames(buildNameList) {
  const buildingNameListWithoutGenericTerms = [];
  for (const name of buildNameList) {
      if (name in buildingGenericTerms) {
          buildingNameListWithoutGenericTerms.push(...buildingGenericTerms[name]);
      } else {
          buildingNameListWithoutGenericTerms.push(name);
      }
  }
  return buildingNameListWithoutGenericTerms;
}