function getBlueprintList(encodedBlueprintStr) {
  // Remove the initial "0" character from the blueprint string
  const strippedStr = encodedBlueprintStr.slice(1);
  
  // Decode base64 to bytes
  const decodedData = atob(strippedStr);
  
  // Convert decoded string to Uint8Array for decompression
  const byteArray = new Uint8Array(decodedData.length);
  for (let i = 0; i < decodedData.length; i++) {
    byteArray[i] = decodedData.charCodeAt(i);
  }
  
  // Decompress using pako (zlib implementation)
  const decompressedData = pako.inflate(byteArray, { to: 'string' });
  
  // Parse JSON
  const rawBlueprintJson = JSON.parse(decompressedData);
  
  const blueprintNames = [];
  const blueprintJsons = [];
  
  getLabelAndBlueprint(blueprintNames, blueprintJsons, rawBlueprintJson);
  
  return [blueprintNames, blueprintJsons];
}

function getLabelAndBlueprint(blueprintNames, blueprintJsons, rawBlueprintJson) {
  if ("blueprint" in rawBlueprintJson) {
    blueprintNames.push(
      rawBlueprintJson.blueprint.label || ""
    );
    blueprintJsons.push(rawBlueprintJson.blueprint);
  } 
  else if ("blueprint_book" in rawBlueprintJson) {
    for (const rawBlueprint of rawBlueprintJson.blueprint_book.blueprints) {
      getLabelAndBlueprint(blueprintNames, blueprintJsons, rawBlueprint);
    }
  }
}

// Constants
const DIRECTION_OFFSET = [
    [0, -1], [1, -1], [1, 0], [1, 1], 
    [0, 1], [-1, 1], [-1, 0], [-1, -1]
];

function getBlueprint(blueprintJson, bboxBorderNWSE = [3, 3, 3, 3]) {
    // Convert blueprint to string and encode
    const blueprintJsonStr = JSON.stringify({ blueprint: blueprintJson });
    const compressedData = pako.deflate(blueprintJsonStr, { level: 9 });
    
    // Convert to base64
    const encodedBlueprintStr = btoa(
        String.fromCharCode.apply(null, compressedData)
    );
    
    const entities = getSimplifiedEntities(blueprintJson);
    const [bboxWidth, bboxHeight] = getSizeAndNormalizeEntities(entities, bboxBorderNWSE);
    
    return {
        entities: entities,
        bboxWidth: bboxWidth,
        bboxHeight: bboxHeight,
        encodedBlueprintStr: encodedBlueprintStr,
        cache: {}
    };
}

function getSimplifiedEntities(blueprintJson) {
    // Create deep copy of blueprint
    blueprintJson = JSON.parse(JSON.stringify(blueprintJson));
    
    if (!("entities" in blueprintJson)) {
        return [];
    }

    for (const e of blueprintJson.entities) {
        // Set default direction if not present
        if (!("direction" in e)) {
            e.direction = 0;
        }
        e.direction = parseInt(e.direction);

        // Convert position to array format
        e.pos = [parseFloat(e.position.x), parseFloat(e.position.y)];
        
        // Special case for offshore pump
        if (e.name === "offshore-pump") {
            e.pos = e.pos.map((coord, i) => 
                coord + 0.5 * DIRECTION_OFFSET[e.direction][i]
            );
        }
    }

    return blueprintJson.entities;
}

function getSizeAndNormalizeEntities(entities, bboxBorderNWSE) {
    if (entities.length === 0) {
        return [1, 1];
    }

    const entityBboxes = [];
    for (const e of entities) {
        if (e.name in BUILDING_SIZES) {
            let [sizeX, sizeY] = BUILDING_SIZES[e.name];
            if (e.direction % 2 !== 0) {
                [sizeX, sizeY] = [sizeY, sizeX];
            }
            entityBboxes.push([
                e.pos[0] - sizeX/2, 
                e.pos[1] - sizeY/2,
                e.pos[0] + sizeX/2, 
                e.pos[1] + sizeY/2
            ]);
        }
    }

    // Calculate bounding box
    const bbox = [
        Math.min(...entityBboxes.map(box => box[0])),
        Math.min(...entityBboxes.map(box => box[1])),
        Math.max(...entityBboxes.map(box => box[2])),
        Math.max(...entityBboxes.map(box => box[3]))
    ];

    // Apply border
    bbox[0] -= bboxBorderNWSE[1];
    bbox[1] -= bboxBorderNWSE[0];
    bbox[2] += bboxBorderNWSE[3];
    bbox[3] += bboxBorderNWSE[2];

    const bboxWidth = bbox[2] - bbox[0];
    const bboxHeight = bbox[3] - bbox[1];

    // Normalize entity positions
    for (const e of entities) {
        if ("pos" in e) {
            e.pos[0] -= bbox[0];
            e.pos[1] -= bbox[1];
        }
    }

    return [bboxWidth, bboxHeight];
}

function get_current_blueprint_entity_count(){
    const entityCount = {};
    for (const entity of current_blueprint.entities) {
      entityCount[entity.name] = (entityCount[entity.name] || 0) + 1;
    }
    return Object.entries(entityCount).sort((a, b) => b[1] - a[1]);
}

function drawBlueprint(blueprint, settings, svgWidthInMm = 300, aspectRatio = null) {
    const metadataStr = `<metadata generated_with="https://piebro.github.io/factorio-blueprint-visualizer"><settings>${JSON.stringify(settings)}</settings><blueprint>${blueprint.encodedBlueprintStr}</blueprint></metadata>`;

    settings = preProcessSettings(settings);
    const background = settings[0][1];

    const defaultBboxProp = {
        scale: null,
        rx: null,
        ry: null
    };

    const dwg = getDrawing(blueprint.bboxWidth, blueprint.bboxHeight, background, metadataStr, svgWidthInMm, aspectRatio);

    for (const [settingName, settingOptions] of settings) {
        if (settingName === "background") {
            continue;
        }

        else if (settingName === "svg") {
            appendGroup(dwg, settingOptions, ["bbox-scale", "bbox-rx", "bbox-ry"]);
            for (const bboxPropKey of ["bbox-scale", "bbox-rx", "bbox-ry"]) {
                if (bboxPropKey in settingOptions) {
                    defaultBboxProp[bboxPropKey.slice(5)] = settingOptions[bboxPropKey];
                }
            }
        }

        else if (settingName === "bbox") {
            drawEntitiesBbox(dwg, blueprint.entities, settingOptions, defaultBboxProp);
        }

        else if (settingName === "belts") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesBelt(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "underground-belts") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesUndergroundBelt(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "pipes") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesPipes(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "underground-pipes") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesUndergroundPipes(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "inserters") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesInserter(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "rails") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesRails(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "electricity") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesElectricity(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "red-circuits") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesCircuit(blueprint.entities, "red");
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else if (settingName === "green-circuits") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesCircuit(blueprint.entities, "green");
            }
            drawLines(dwg, blueprint.cache[settingName], settingOptions);
        }

        else {
            console.log("unknown setting name:", settingName);
        }
    }

    for (let i = 0; i < dwg.groupsToClose; i++) {
        dwg.parts.push('</g>');
    }
    dwg.parts.push('</svg>');
    return dwg.parts.join('');
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
        if (name in BUILDING_GENERIC_TERMS) {
            buildingNameListWithoutGenericTerms.push(...BUILDING_GENERIC_TERMS[name]);
        } else {
            buildingNameListWithoutGenericTerms.push(name);
        }
    }
    return buildingNameListWithoutGenericTerms;
}

function getDrawing(bboxWidth, bboxHeight, backgroundColor = "#dddddd", metadataStr = null, svgWidthInMm = 300, aspectRatio = null) {
    if (aspectRatio !== null) {
        const realRatio = bboxWidth / bboxHeight;
        const targetRatio = aspectRatio[0] / aspectRatio[1];

        let newBboxWidth = bboxWidth;
        let newBboxHeight = bboxHeight;
        let translate;

        if (realRatio < targetRatio) {
            newBboxWidth = targetRatio * bboxHeight;
            translate = [(newBboxWidth - bboxWidth) / 2, 0];
        } else {
            newBboxHeight = (1 / targetRatio) * bboxWidth;
            translate = [0, (newBboxHeight - bboxHeight) / 2];
        }

        bboxWidth = newBboxWidth;
        bboxHeight = newBboxHeight;
    }

    const dwg = {
        groupsToClose: 0,
        parts: [`<svg baseProfile="tiny" height="${svgWidthInMm * bboxHeight / bboxWidth}mm" version="1.2" viewBox="0,0,${bboxWidth},${bboxHeight}" width="${svgWidthInMm}mm" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">`]
    };

    if (metadataStr !== null) {
        dwg.parts.push(metadataStr);
    }

    if (aspectRatio !== null) {
        appendGroup(dwg, { transform: `translate(${translate[0]} ${translate[1]})` });
    }

    if (backgroundColor !== null) {
        dwg.parts.push(`<rect fill="${backgroundColor}" height="10000" width="10000" x="-100" y="-100" />`);
    }

    return dwg;
}

function appendGroup(dwg, svgSetting, denyList = []) {
    dwg.parts.push('<g');
    appendSvgSetting(dwg, svgSetting, denyList);
    dwg.parts.push('>');
    dwg.groupsToClose += 1;
}

function drawLines(dwg, lines, svgSetting) {
    dwg.parts.push('<path');
    appendSvgSetting(dwg, svgSetting);
    dwg.parts.push(' d="');
    for (const [p1, p2] of lines) {
        dwg.parts.push(`M${p1[0]} ${p1[1]} ${p2[0]} ${p2[1]}`);
    }
    dwg.parts.push('"/>');
}

function appendSvgSetting(dwg, svgSetting, denyList = []) {
    for (const [key, value] of Object.entries(svgSetting)) {
        if (!denyList.includes(key)) {
            dwg.parts.push(` ${key}="${value}"`);
        }
    }
}

function drawRect(dwg, mid, size, scale, rx, ry) {
    if (scale !== null) {
        size = [size[0] * scale, size[1] * scale];
    }

    dwg.parts.push(`<rect height="${size[1]}" width="${size[0]}" x="${mid[0] - size[0]/2}" y="${mid[1] - size[1]/2}"`);
    
    if (rx !== null) {
        dwg.parts.push(` rx="${rx}" `);
    }
    if (ry !== null) {
        dwg.parts.push(` ry="${ry}" `);
    }

    dwg.parts.push('/>');
}

function drawEntitiesBbox(dwg, entities, settings, defaultBboxProp) {
    let bboxEntities;
    if ("allow" in settings) {
        bboxEntities = entities.filter(e => settings.allow.includes(e.name));
    } else if ("deny" in settings) {
        bboxEntities = entities.filter(e => !settings.deny.includes(e.name));
    } else {
        bboxEntities = entities;
    }
    
    const bboxProp = {};
    for (const bboxPropKey of ["bbox-scale", "bbox-rx", "bbox-ry"]) {
        bboxProp[bboxPropKey.slice(5)] = bboxPropKey in settings 
            ? settings[bboxPropKey] 
            : defaultBboxProp[bboxPropKey.slice(5)];
    }

    appendGroup(dwg, settings, ["bbox-scale", "bbox-rx", "bbox-ry", "allow", "deny"]);
    for (const e of bboxEntities) {
        if (e.name in BUILDING_SIZES) {
            let sizeX, sizeY;
            if (e.direction % 4 === 0) {
                [sizeX, sizeY] = BUILDING_SIZES[e.name];
            } else {
                [sizeY, sizeX] = BUILDING_SIZES[e.name];
            }
            drawRect(dwg, e.pos, [sizeX, sizeY], bboxProp.scale, bboxProp.rx, bboxProp.ry);
        }
    }
    dwg.groupsToClose -= 1;
    dwg.parts.push('</g>');
}

function getLinesBelt(entities) {
    const nodes = {};
    const connectConditions = [];

    // First pass: collect nodes and connection conditions
    for (const e of entities) {
        if (["transport-belt", "fast-transport-belt", "express-transport-belt", 
             "underground-belt", "fast-underground-belt", "express-underground-belt"].includes(e.name)) {
            
            const pos = `${e.pos[0]},${e.pos[1]}`; // Use string as object key
            const dir = e.direction;

            // Initialize node if not exists
            if (!(pos in nodes)) {
                nodes[pos] = [false, false, false, false, false, false, false, false];
            }
            nodes[pos][dir] = true;

            // Skip if underground belt input
            if (e.type === "input") continue;
            
            console.log(e.name, e.pos, e.direction);
            console.log(DIRECTION_OFFSET[dir][0], DIRECTION_OFFSET[dir][1]);
            // Calculate target position
            const targetPos = [
                e.pos[0] + DIRECTION_OFFSET[dir][0],
                e.pos[1] + DIRECTION_OFFSET[dir][1]
            ];
            const targetPosKey = `${targetPos[0]},${targetPos[1]}`;

            // Add connection conditions for three possible directions
            for (const targetDir of [(dir - 2 + 8) % 8, dir, (dir + 2) % 8]) {
                connectConditions.push([pos, dir, targetPosKey, targetDir]);
            }
        }
    }

    // Get initial lines from nodes and connection conditions
    const lines = getLinesNodesAndConnectConditions(nodes, connectConditions, false, false, false, false);

    // Handle splitters
    for (const e of entities) {
        if (["splitter", "fast-splitter", "express-splitter"].includes(e.name)) {
            const dir = e.direction;
            const offset = [
                0.5 * DIRECTION_OFFSET[(dir + 2) % 8][0],
                0.5 * DIRECTION_OFFSET[(dir + 2) % 8][1]
            ];

            // Calculate positions
            const pos12 = [
                [e.pos[0] - offset[0], e.pos[1] - offset[1]],
                [e.pos[0] + offset[0], e.pos[1] + offset[1]]
            ];
            const fromPos12 = pos12.map(pos => [
                pos[0] - DIRECTION_OFFSET[dir][0],
                pos[1] - DIRECTION_OFFSET[dir][1]
            ]);
            const toPos12 = pos12.map(pos => [
                pos[0] + DIRECTION_OFFSET[dir][0],
                pos[1] + DIRECTION_OFFSET[dir][1]
            ]);

            // Check node existence and conditions
            const toPosInNodes = toPos12.map((pos, i) => {
                const key = `${pos[0]},${pos[1]}`;
                return key in nodes && !nodes[key][(dir - 4 + 8) % 8];
            });
            const fromPosInNodes = fromPos12.map((pos, i) => {
                const key = `${pos[0]},${pos[1]}`;
                return key in nodes && nodes[key][dir];
            });

            // Add lines based on conditions
            for (let i = 0; i < 2; i++) {
                if (toPosInNodes[i] && (!fromPosInNodes[(i + 1) % 2] || fromPosInNodes[i])) {
                    lines.push([pos12[i], toPos12[i]]);
                }

                if (fromPosInNodes[i]) {
                    lines.push([fromPos12[i], pos12[i]]);

                    if (toPosInNodes[(i + 1) % 2]) {
                        lines.push([pos12[i], toPos12[(i + 1) % 2]]);
                    }
                }
            }
        }
    }

    return lines;
}

function getLinesNodesAndConnectConditions(nodes, connectConditions, drawNodes = false, drawTargetPos = false, setSelfFalse = true, setTargetFalse = true) {
    if (drawNodes) {
        const lines = Object.keys(nodes).map(pos => {
            const [x, y] = pos.split(',').map(Number);
            return [[x, y], [x, y]];
        });
        if (drawTargetPos) {
            lines.push(...connectConditions.map(([_, __, targetPos]) => {
                const [x, y] = targetPos.split(',').map(Number);
                return [[x, y], [x, y]];
            }));
        }
        return lines;
    }

    const lines = [];
    for (const [srcPos, srcDir, targetPos, targetDir] of connectConditions) {
        if (nodes[srcPos][srcDir] && targetPos in nodes && nodes[targetPos][targetDir]) {
            const [x1, y1] = srcPos.split(',').map(Number);
            const [x2, y2] = targetPos.split(',').map(Number);
            lines.push([[x1, y1], [x2, y2]]);
            
            if (setSelfFalse) nodes[targetPos][targetDir] = false;
            if (setTargetFalse) nodes[srcPos][srcDir] = false;
        }
    }
    return lines;
}

function getLinesInserter(entities) {
    const lines = [];
    for (const e of entities) {
        if (["burner-inserter", "inserter", "fast-inserter", "filter-inserter", "stack-inserter", "stack-filter-inserter"].includes(e.name)) {
            const p0 = [
                e.pos[0] + DIRECTION_OFFSET[e.direction][0],
                e.pos[1] + DIRECTION_OFFSET[e.direction][1]
            ];
            const p1 = [
                e.pos[0] - DIRECTION_OFFSET[e.direction][0],
                e.pos[1] - DIRECTION_OFFSET[e.direction][1]
            ];
            lines.push([p0, p1]);
        } 
        else if (e.name === "long-handed-inserter") {
            const p0 = [
                e.pos[0] + 2 * DIRECTION_OFFSET[e.direction][0],
                e.pos[1] + 2 * DIRECTION_OFFSET[e.direction][1]
            ];
            const p1 = [
                e.pos[0] - 2 * DIRECTION_OFFSET[e.direction][0],
                e.pos[1] - 2 * DIRECTION_OFFSET[e.direction][1]
            ];
            lines.push([p0, p1]);
        }
    }
    return lines;
}

function getLinesPipes(entities) {
    const nodes = {};
    const connectConditions = [];

    for (const e of entities) {
        if (!(e.name in BUILDING_PIPE_CONNECTIONS)) {
            continue;
        }

        let recipeDirectionChange = 0;
        if (["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"].includes(e.name)) {
            if (!("recipe" in e)) {
                continue;
            }

            if (e.recipe in ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE) {
                recipeDirectionChange = ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE[e.recipe];
            } else {
                continue;
            }
        }

        for (const connection of BUILDING_PIPE_CONNECTIONS[e.name]) {
            const rotatedPos = rotate((e.direction + recipeDirectionChange) % 8, connection.pos);
            const pos = [
                e.pos[0] + rotatedPos[0],
                e.pos[1] + rotatedPos[1]
            ];
            const dir = (e.direction + connection.direction + recipeDirectionChange) % 8;
            
            const posKey = `${pos[0]},${pos[1]}`;
            if (!(posKey in nodes)) {
                nodes[posKey] = [false, false, false, false, false, false, false, false];
            }
            nodes[posKey][dir] = true;

            const targetPos = [
                pos[0] + DIRECTION_OFFSET[dir][0],
                pos[1] + DIRECTION_OFFSET[dir][1]
            ];
            const targetDir = (dir + 4) % 8;
            connectConditions.push([posKey, dir, `${targetPos[0]},${targetPos[1]}`, targetDir]);
        }
    }

    return getLinesNodesAndConnectConditions(nodes, connectConditions);
}

function getLinesUndergroundPipes(entities, maxLength = 11) {
    const nodes = {};
    for (const e of entities) {
        if (e.name === "pipe-to-ground") {
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            nodes[posKey] = (e.direction + 4) % 8;
        }
    }

    const lines = [];
    for (const [posKey, dir] of Object.entries(nodes)) {
        if (dir < 4) {
            const [x, y] = posKey.split(',').map(Number);
            const dirOffset = DIRECTION_OFFSET[dir];
            
            for (let i = 1; i < maxLength; i++) {
                const targetPos = [
                    x + i * dirOffset[0],
                    y + i * dirOffset[1]
                ];
                const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
                
                if (targetPosKey in nodes && nodes[targetPosKey] === (dir + 4) % 8) {
                    lines.push([[x, y], targetPos]);
                    break;
                }
            }
        }
    }
    return lines;
}

function rotate(angle, pos) {
    if (angle === 0) {
        return pos;
    } else if (angle === 2) {
        return [-pos[1], pos[0]];
    } else if (angle === 4) {
        return [-pos[0], -pos[1]];
    } else if (angle === 6) {
        return [pos[1], -pos[0]];
    }
}

function getLinesRails(entities) {
    const lines = [];
    for (const e of entities) {
        if (e.name === "straight-rail") {
            const dir = e.direction;
            if (dir % 2 === 0) {
                const p0 = [
                    e.pos[0] + DIRECTION_OFFSET[dir][0],
                    e.pos[1] + DIRECTION_OFFSET[dir][1]
                ];
                const p1 = [
                    e.pos[0] - DIRECTION_OFFSET[dir][0],
                    e.pos[1] - DIRECTION_OFFSET[dir][1]
                ];
                lines.push([p0, p1]);
            } else {
                const p0 = [
                    e.pos[0] + DIRECTION_OFFSET[(dir - 1 + 8) % 8][0],
                    e.pos[1] + DIRECTION_OFFSET[(dir - 1 + 8) % 8][1]
                ];
                const p1 = [
                    e.pos[0] + DIRECTION_OFFSET[(dir + 1) % 8][0],
                    e.pos[1] + DIRECTION_OFFSET[(dir + 1) % 8][1]
                ];
                lines.push([p0, p1]);
            }
        } 
        else if (e.name === "curved-rail") {
            const dir = e.direction;
            if (dir % 2 === 0) {
                lines.push([
                    [
                        e.pos[0] + rotate(dir, [-2, -3])[0],
                        e.pos[1] + rotate(dir, [-2, -3])[1]
                    ],
                    e.pos
                ]);
                lines.push([
                    e.pos,
                    [
                        e.pos[0] + rotate(dir, [1, 4])[0],
                        e.pos[1] + rotate(dir, [1, 4])[1]
                    ]
                ]);
            } else {
                lines.push([
                    [
                        e.pos[0] + rotate(dir - 1, [2, -3])[0],
                        e.pos[1] + rotate(dir - 1, [2, -3])[1]
                    ],
                    e.pos
                ]);
                lines.push([
                    e.pos,
                    [
                        e.pos[0] + rotate(dir - 1, [-1, 4])[0],
                        e.pos[1] + rotate(dir - 1, [-1, 4])[1]
                    ]
                ]);
            }
        }
    }
    return lines;
}

function getLinesCircuit(entities, circuitColor) {
    const lines = [];
    for (const e of entities) {
        if ("connections" in e) {
            const connectedEntityIds = [];
            if ("1" in e.connections && circuitColor in e.connections["1"]) {
                connectedEntityIds.push(...e.connections["1"][circuitColor].map(i => i.entity_id));
            }
            if ("2" in e.connections && circuitColor in e.connections["2"]) {
                connectedEntityIds.push(...e.connections["2"][circuitColor].map(i => i.entity_id));
            }
            lines.push(...connectedEntityIds.map(n => [e.pos, entities[n-1].pos]));
        }
    }
    return lines;
}

function getLinesElectricity(entities) {
    const lines = [];
    for (const e of entities) {
        if ("neighbours" in e) {
            lines.push(...e.neighbours.map(n => [e.pos, entities[n-1].pos]));
        }
    }
    return lines;
}

function getLinesUndergroundBelt(entities, entityName = null, maxLength = null) {
    if (entityName === null && maxLength === null) {
        const lines = getLinesUndergroundBelt(entities, "underground-belt", 6);
        lines.push(...getLinesUndergroundBelt(entities, "fast-underground-belt", 8));
        lines.push(...getLinesUndergroundBelt(entities, "express-underground-belt", 10));
        return lines;
    }

    const nodesInput = {};
    const nodesOutput = {};
    
    for (const e of entities) {
        if (e.name === entityName) {
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            if (e.type === "input") {
                nodesInput[posKey] = e.direction;
            } else {
                nodesOutput[posKey] = e.direction;
            }
        }
    }

    const lines = [];
    for (const [posKey, dir] of Object.entries(nodesInput)) {
        const [x, y] = posKey.split(',').map(Number);
        const dirOffset = DIRECTION_OFFSET[dir];
        
        for (let i = 1; i < maxLength; i++) {
            const targetPos = [
                x + i * dirOffset[0],
                y + i * dirOffset[1]
            ];
            const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
            
            if (targetPosKey in nodesOutput && nodesOutput[targetPosKey] === dir) {
                lines.push([[x, y], targetPos]);
                break;
            }
        }
    }

    return lines;
}
