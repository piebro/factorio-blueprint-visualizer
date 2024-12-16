const DIRECTION_OFFSET = [
    [0, -1], [1, -1], [1, 0], [1, 1], 
    [0, 1], [-1, 1], [-1, 0], [-1, -1]
];

const DIRECTION_4_TO_OFFSET = [[0, -1], [1, 0], [0, 1], [-1, 0]];

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

function getBlueprint(blueprintJson, bboxBorderNWSE = [3, 3, 3, 3]) {
    // Convert blueprint to string and encode
    const blueprintJsonStr = JSON.stringify({ blueprint: blueprintJson });
    const compressedData = pako.deflate(blueprintJsonStr, { level: 9 });
    
    // Convert to base64
    const encodedBlueprintStr = btoa(
        String.fromCharCode.apply(null, compressedData)
    );
    
    const entities = getSimplifiedEntities(blueprintJson);
    const [bboxWidth, bboxHeight, posOffset] = getSizeAndNormalizeEntities(entities, bboxBorderNWSE);
    
    return {
        entities: entities,
        bboxWidth: bboxWidth,
        bboxHeight: bboxHeight,
        posOffset: posOffset,
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

    directions = {}
    for (const e of blueprintJson.entities) {
        // Set default direction if not present
        if (!("direction" in e)) {
            e.direction = 0;
        }
        e.direction = parseInt(e.direction);
        
        // Count directions
        directions[e.direction] = (directions[e.direction] || 0) + 1;

        // Convert position to array format
        e.pos = [parseFloat(e.position.x), parseFloat(e.position.y)];
        
        if (e.name in entityNameToProperties) {
            let [sizeX, sizeY] = entityNameToProperties[e.name].size;
            const angleRad = (e.direction * Math.PI) / 8;
            const cos = Math.cos(angleRad);
            const sin = Math.sin(angleRad);
            
            // Calculate rotated corners relative to center
            e.bbox = [
                [-sizeX/2, -sizeY/2], // top-left
                [sizeX/2, -sizeY/2],  // top-right
                [sizeX/2, sizeY/2],   // bottom-right
                [-sizeX/2, sizeY/2]   // bottom-left
            ].map(([x, y]) => [
                x * cos - y * sin + e.pos[0],
                x * sin + y * cos + e.pos[1]
            ]);
        }
    }

    return blueprintJson.entities;
}

function getSizeAndNormalizeEntities(entities, bboxBorderNWSE) {
    if (entities.length === 0) {
        return [1, 1];
    }

    const entityBboxes = entities.filter(e => "bbox" in e).map(e => e.bbox);

    // Calculate bounding box from 4-point polygons
    const bbox = [
        Math.min(...entityBboxes.flatMap(box => box.map(point => point[0]))), // minX
        Math.min(...entityBboxes.flatMap(box => box.map(point => point[1]))), // minY
        Math.max(...entityBboxes.flatMap(box => box.map(point => point[0]))), // maxX
        Math.max(...entityBboxes.flatMap(box => box.map(point => point[1])))  // maxY
    ];

    // Apply border
    bbox[0] -= bboxBorderNWSE[1];
    bbox[1] -= bboxBorderNWSE[0];
    bbox[2] += bboxBorderNWSE[3];
    bbox[3] += bboxBorderNWSE[2];

    const bboxWidth = bbox[2] - bbox[0];
    const bboxHeight = bbox[3] - bbox[1];

    // Normalize entity positions
    // for (const e of entities) {
    //     if ("pos" in e) {
    //         e.pos[0] = Math.round((e.pos[0] - bbox[0]) * 10000) / 10000;
    //         e.pos[1] = Math.round((e.pos[1] - bbox[1]) * 10000) / 10000;
    //     }
    //     if ("bbox" in e) {
    //         // Update each point of the bbox
    //         e.bbox = e.bbox.map(point => [
    //             point[0] - bbox[0],
    //             point[1] - bbox[1]
    //         ]);
    //     }
    // }

    const posOffset = [-bbox[0], -bbox[1]];

    return [bboxWidth, bboxHeight, posOffset];
}

function getCurrentBlueprintEntityCount(currentBlueprint){
    const entityCount = {};
    for (const entity of currentBlueprint.entities) {
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
            drawEntitiesBbox(dwg, blueprint.entities, blueprint.posOffset, settingOptions, defaultBboxProp);
        }

        else if (settingName === "belts") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesBelt(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "underground-belts") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesUndergroundBelt(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "pipes") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesPipesOrHeatPipes(blueprint.entities, itemToPipeTargetPositions);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "underground-pipes") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesUndergroundPipes(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "heat-pipes") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesPipesOrHeatPipes(blueprint.entities, itemToHeatTargetPositions);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "inserters") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesInserter(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "rails") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesRails(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "electricity") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesElectricity(blueprint.entities);
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "red-circuits") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesCircuit(blueprint.entities, "red");
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
        }

        else if (settingName === "green-circuits") {
            if (!(settingName in blueprint.cache)) {
                blueprint.cache[settingName] = getLinesCircuit(blueprint.entities, "green");
            }
            drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingOptions);
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

function drawLines(dwg, lines, posOffset, svgSetting) {
    dwg.parts.push('<path');
    appendSvgSetting(dwg, svgSetting);
    dwg.parts.push(' d="');
    for (const [p1, p2] of lines) {
        dwg.parts.push(`M${p1[0] + posOffset[0]} ${p1[1] + posOffset[1]} ${p2[0] + posOffset[0]} ${p2[1] + posOffset[1]}`);
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

function drawRect(dwg, bbox, posOffset, scale, rx, ry) {
    if (scale !== null) {
        // Calculate center point
        const centerX = bbox.reduce((sum, point) => sum + point[0], 0) / 4;
        const centerY = bbox.reduce((sum, point) => sum + point[1], 0) / 4;
        
        // Scale points around center
        bbox = bbox.map(point => [
            centerX + (point[0] - centerX) * scale,
            centerY + (point[1] - centerY) * scale
        ]);
    }

    // Create SVG polygon points string
    const pointsStr = bbox.map(point => `${point[0] + posOffset[0]},${point[1] + posOffset[1]}`).join(' ');
    
    dwg.parts.push(`<polygon points="${pointsStr}"`);
    
    if (rx !== null || ry !== null) {
        console.warn('rx and ry are not supported for rotated rectangles');
    }

    dwg.parts.push('/>');
}

function drawEntitiesBbox(dwg, entities, posOffset, settings, defaultBboxProp) {
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
        if ("bbox" in e) {
            drawRect(dwg, e.bbox, posOffset, bboxProp.scale, bboxProp.rx, bboxProp.ry);
        }
    }
    dwg.groupsToClose -= 1;
    dwg.parts.push('</g>');
}

function getLinesUndergroundBelt(entities) {
    const nodesInput = {};
    const nodesOutput = {};
    for (const entityName of ["underground-belt", "fast-underground-belt", "express-underground-belt", "turbo-underground-belt"]) {
        nodesInput[entityName] = {};
        nodesOutput[entityName] = {};
    }

    for (const e of entities) {
        if (e.name === "underground-belt" || e.name === "fast-underground-belt" || e.name === "express-underground-belt" || e.name === "turbo-underground-belt") {
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            if (e.type === "input") {
                nodesInput[e.name][posKey] = e.direction;
            } else {
                nodesOutput[e.name][posKey] = e.direction;
            }
        }
    }

    const lines = [];
    for (const [entityName, maxLength] of [["underground-belt", 6], ["fast-underground-belt", 8], ["express-underground-belt", 10], ["turbo-underground-belt", 12]]) {
        for (const [posKey, dir] of Object.entries(nodesInput[entityName])) {
            
            if (dir === 0) {
                offset = [0, 1];
            } else if (dir === 4) {
                offset = [1, 0];
            } else if (dir === 8) {
                offset = [0, -1];
            } else if (dir === 12) {
                offset = [-1, 0];
            }

            const [x, y] = posKey.split(',').map(Number);
            for (let i = 1; i < maxLength; i++) {
                const targetPos = [
                    x + i * offset[0],
                    y + i * offset[1]
                ];
                const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
                if (targetPosKey in nodesOutput[entityName] && nodesOutput[entityName][targetPosKey] === dir) {
                    lines.push([[x, y], targetPos]);
                    break;
                }
            }
        }
    }
    return lines;
}

function getLinesBelt(entities) {
    const nodes = {};

    // collect nodes
    for (const e of entities) {
        if (e.name === "transport-belt" || e.name === "fast-transport-belt" || e.name === "express-transport-belt" || e.name === "turbo-transport-belt"
            || e.name === "underground-belt" || e.name === "fast-underground-belt" || e.name === "express-underground-belt" || e.name === "turbo-underground-belt"
        ) {
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            const dir = Math.floor(e.direction / 4);
            const offset = DIRECTION_4_TO_OFFSET[dir];
            const targetPos = [e.pos[0] + offset[0], e.pos[1] + offset[1]];
            if (e.type === "input") {
                nodes[posKey] = [e.pos, null];
            } else {
                nodes[posKey] = [e.pos, targetPos];
            }
        }
        
    }
    
    // create lines
    const lines = [];
    for (const [pos, targetPos] of Object.values(nodes)) {   
        if (targetPos === null) continue;
        const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
        if (targetPosKey in nodes) {
            lines.push([pos, targetPos]);
        }
    }

    // Handle splitters
    for (const e of entities) {
        if (e.name === "splitter" || e.name === "fast-splitter" || e.name === "express-splitter" || e.name === "turbo-splitter") {
            const dir = Math.floor(e.direction / 4);
            const offset = DIRECTION_4_TO_OFFSET[dir];
            const offset90 = DIRECTION_4_TO_OFFSET[(dir + 1) % 4];
            const offset270 = DIRECTION_4_TO_OFFSET[(dir + 3) % 4];
            const pos1 = [e.pos[0] + offset90[0]/2, e.pos[1] + offset90[1]/2];
            const pos2 = [e.pos[0] + offset270[0]/2, e.pos[1] + offset270[1]/2];

            const inputPos1 = [pos1[0] - offset[0], pos1[1] - offset[1]];
            const inputPos2 = [pos2[0] - offset[0], pos2[1] - offset[1]];

            const inputPos1Key = `${inputPos1[0]},${inputPos1[1]}`;
            const inputPos2Key = `${inputPos2[0]},${inputPos2[1]}`;

            if (inputPos1Key in nodes) {
                lines.push([inputPos1, pos1]);
                lines.push([inputPos1, pos2]);
            }

            if (inputPos2Key in nodes) {
                lines.push([inputPos2, pos1]);
                lines.push([inputPos2, pos2]);
            }

            const outputPos1 = [pos1[0] + offset[0], pos1[1] + offset[1]];
            const outputPos2 = [pos2[0] + offset[0], pos2[1] + offset[1]];

            const outputPos1Key = `${outputPos1[0]},${outputPos1[1]}`;
            const outputPos2Key = `${outputPos2[0]},${outputPos2[1]}`;

            if (outputPos1Key in nodes) {
                lines.push([pos1, outputPos1]);
            }

            if (outputPos2Key in nodes) {
                lines.push([pos2, outputPos2]);
            }

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

function orderPoints(pos1, pos2) {
    // Sort the positions by comparing first x then y
    if (pos1[0] < pos2[0]) {
        return [pos1, pos2];
    } else if (pos1[0] > pos2[0]) {
        return [pos2, pos1];
    } else {
        // x coordinates are equal, compare y
        return pos1[1] <= pos2[1] ? [pos1, pos2] : [pos2, pos1];
    }
}

function getLinesPipesOrHeatPipes(entities, targetPositionsMap) {
    function rotate(angle, pos) {
        if (angle === 0) {
            return pos;
        } else if (angle === 1) {
            return [-pos[1], pos[0]];
        } else if (angle === 2) {
            return [-pos[0], -pos[1]];
        } else if (angle === 3) {
            return [pos[1], -pos[0]];
        }
    }

    const nodes = {};

    for (const e of entities) {
        if (!(e.name in targetPositionsMap)) {
            continue;
        } 
        for (let [connectionPos, targetPos] of targetPositionsMap[e.name]) {
            
            // Special check for assembling machines with fluid recipes
            if (e.name === "assembling-machine-2" || e.name === "assembling-machine-3" || e.name === "biochamber") {
                if (!(e.recipe in fluidRecipes)) {
                    continue;
                }
            }
            const dir = Math.floor(e.direction / 4)
            connectionPos = rotate(dir, connectionPos);
            targetPos = rotate(dir, targetPos);
            
            connectionPos = [
                e.pos[0] + connectionPos[0],
                e.pos[1] + connectionPos[1]
            ];
            targetPos = [
                e.pos[0] + targetPos[0],
                e.pos[1] + targetPos[1]
            ];
            
            const connectionPosKey = `${connectionPos[0]},${connectionPos[1]}`;
            if (!(connectionPosKey in nodes)) {
                nodes[connectionPosKey] = [connectionPos, [targetPos]];
            } else {
                nodes[connectionPosKey][1].push(targetPos);
            }
        }
    }

    // create lines
    const lines = [];
    const linesCache = {};
    for (const [pos, targetPosList] of Object.values(nodes)) {   
        if (targetPosList === null) continue;
        for (const targetPos of targetPosList) {
            // Use the new orderPoints function
            const [p1, p2] = orderPoints(pos, targetPos);
            
            // Create a unique key for the line 
            const lineKey = `${p1[0]},${p1[1]}-${p2[0]},${p2[1]}`;
            const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
            
            if (targetPosKey in nodes && !(lineKey in linesCache)) {
                linesCache[lineKey] = true;
                lines.push([p1, p2]);
            }
        }
    }

    return lines;
}

function getLinesUndergroundPipes(entities, maxLength = 11) {
    const nodes = {};
    for (const e of entities) {
        if (e.name === "pipe-to-ground") {
            const dirOpposite = (Math.floor(e.direction / 4) + 2) % 4
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            nodes[posKey] = [e.pos, dirOpposite]
        }
    }

    const lines = [];
    for (const [pos, dirOpposite] of Object.values(nodes)) {
        const offset = DIRECTION_4_TO_OFFSET[dirOpposite];
        for (let i = 1; i < maxLength; i++) {
            const targetPos = [
                pos[0] + i * offset[0], 
                pos[1] + i * offset[1]
            ];
            const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
            if (targetPosKey in nodes && nodes[targetPosKey][1] === (dirOpposite + 2) % 4) {
                lines.push([pos, targetPos]);
                break;
            }
        }   
    }
    return lines;
}






function getLinesRails(entities) {

    function mirrorOffsetsVertical(offsets) {
        return [[-offsets[0][0], offsets[0][1]], [-offsets[1][0], offsets[1][1]]];
    }
    
    function rotateOffsets90Degrees(offsets, numTimes = 1) {
        for (let i = 0; i < numTimes; i++) {
            offsets = [[-offsets[0][1], offsets[0][0]], [-offsets[1][1], offsets[1][0]]];
        }
        return offsets;
    }

    const lines = [];
    for (const e of entities) {
        if (e.name === "straight-rail" || e.name === "elevated-straight-rail") {
            const dir = e.direction;
            let offsets = [[0, 1], [0, -1]];
            if (dir === 2) {
                offsets = [[-1, 1], [1, -1]];
            }
            else if (dir === 4) {
                offsets = [[1, 0], [-1, 0]];
            }
            else if (dir === 6) {
                offsets = [[1, 1], [-1, -1]];
            }
            lines.push([
                [e.pos[0]+offsets[0][0], e.pos[1]+offsets[0][1]],
                [e.pos[0]+offsets[1][0], e.pos[1]+offsets[1][1]]
            ]);
        } else if (e.name === "curved-rail-a" || e.name === "curved-rail-b" || e.name === "half-diagonal-rail" || e.name === "elevated-curved-rail-a" || e.name === "elevated-curved-rail-b" || e.name === "elevated-half-diagonal-rail") {
            const dir = e.direction;
            let offsets;
            if (e.name === "curved-rail-a" || e.name === "elevated-curved-rail-a") {
                offsets = [[0, 3], [-1, -3]];
            } else if (e.name === "curved-rail-b" || e.name === "elevated-curved-rail-b") {
                offsets = [[1, 2], [-2, -2]];
            } else if (e.name === "half-diagonal-rail" || e.name === "elevated-half-diagonal-rail") {
                offsets = [[1, 2], [-1, -2]];
            }

            let offsetsMirrorVertical = mirrorOffsetsVertical(offsets);
            if (dir === 2) {
                offsets = offsetsMirrorVertical;
            }
            else if (dir === 4) {
                offsets = rotateOffsets90Degrees(offsets, 1);
            }
            else if (dir === 6) {
                offsets = rotateOffsets90Degrees(offsetsMirrorVertical, 1);
            }
            else if (dir === 8) {
                offsets = rotateOffsets90Degrees(offsets, 2);
            }
            else if (dir === 10) {
                offsets = rotateOffsets90Degrees(offsetsMirrorVertical, 2);
            }
            else if (dir === 12) {
                offsets = rotateOffsets90Degrees(offsets, 3);
            }
            else if (dir === 14) {
                offsets = rotateOffsets90Degrees(offsetsMirrorVertical, 3);
            }
            lines.push([
                [e.pos[0]+offsets[0][0], e.pos[1]+offsets[0][1]],
                e.pos
            ]);
            lines.push([
                e.pos,
                [e.pos[0]+offsets[1][0], e.pos[1]+offsets[1][1]]
            ]);
        }
        else if (e.name === "rail-ramp") {
            const dir = e.direction;
            let offsets = [[-8, 0], [8, 0]];
            if (dir % 8 === 0) {
                offsets = [[0, -8], [0, 8]];
            }
            lines.push([
                [e.pos[0]+offsets[0][0], e.pos[1]+offsets[0][1]],
                [e.pos[0]+offsets[1][0], e.pos[1]+offsets[1][1]]
            ]);
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


