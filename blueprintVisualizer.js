const DIRECTION_4_TO_OFFSET = [[0, -1], [1, 0], [0, 1], [-1, 0]];

const WireType = {GREEN_WIRE: 1, RED_WIRE: 2,  COPPER_WIRE: 5};

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
    getLabelsAndBlueprints(blueprintNames, blueprintJsons, rawBlueprintJson);
    
    return [blueprintNames, blueprintJsons];
}

function getLabelsAndBlueprints(blueprintNames, blueprintJsons, rawBlueprintJson) {
    if ("blueprint" in rawBlueprintJson) {
      blueprintNames.push(
        rawBlueprintJson.blueprint.label || ""
      );
      blueprintJsons.push(rawBlueprintJson.blueprint);
    } 
    else if ("blueprint_book" in rawBlueprintJson) {
      for (const rawBlueprint of rawBlueprintJson.blueprint_book.blueprints) {
        getLabelsAndBlueprints(blueprintNames, blueprintJsons, rawBlueprint);
      }
    }
}

function processBlueprint(blueprintJson, bboxBorderNWSE = [3, 3, 3, 3]) {   
    const blueprintJsonStr = JSON.stringify({ blueprint: blueprintJson });
    const compressedData = pako.deflate(blueprintJsonStr, { level: 9 });
    const encodedBlueprintStr =  btoa(String.fromCharCode.apply(null, compressedData));

    if (!("entities" in blueprintJson)) {
        blueprintJson.entities = []
    }
    if (!("wires" in blueprintJson)) {
        blueprintJson.wires = [];
    }
    if (!("tiles" in blueprintJson)) {
        blueprintJson.tiles = [];
    } else {
        for (const tile of blueprintJson.tiles) {
            tile.pos = [tile.position.x + 0.5, tile.position.y + 0.5];
        }
    }

    getSimplifiedEntities(blueprintJson.entities, blueprintJson.version);
    const [bboxWidth, bboxHeight, posOffset] = getSvgSizeAndPosOffset(blueprintJson.entities, blueprintJson.tiles, bboxBorderNWSE);

    return {
        entities: blueprintJson.entities,
        wires: blueprintJson.wires,
        tiles: blueprintJson.tiles,
        bboxWidth: bboxWidth,
        bboxHeight: bboxHeight,
        posOffset: posOffset,
        encodedBlueprintStr: encodedBlueprintStr,
        cache: {}
    };
}

function getSimplifiedEntities(blueprintJsonEntities, blueprintJsonVersion) {
    for (const e of blueprintJsonEntities) {
        if (!("direction" in e)) {
            e.direction = 0;
        } else {
            // I'm not sure how blueprint versioning works exactly, but this seems to work for the blueprints I've tested
            const factorio_version_1 = (blueprintJsonVersion <= 300000000000000);
            if (factorio_version_1) {
                e.direction = parseInt(e.direction)*2;
            } else {
                e.direction = parseInt(e.direction);
            }
        }
        // Convert position to array format
        e.pos = [e.position.x, e.position.y];
        
        if (e.name in entityNameToProperties) {
            const properties = entityNameToProperties[e.name];
            for (const bboxType of ["size", "selection_size", "collision_size"]) {
                if (bboxType in properties) {
                    let [sizeX, sizeY] = properties[bboxType];
                    if ((e.direction/4) % 2 === 1) {
                        [sizeX, sizeY] = [sizeY, sizeX];
                    }

                    e["bbox_" + bboxType] = [
                        [e.pos[0] - sizeX/2, e.pos[1] - sizeY/2],
                        [e.pos[0] + sizeX/2, e.pos[1] - sizeY/2],
                        [e.pos[0] + sizeX/2, e.pos[1] + sizeY/2],
                        [e.pos[0] - sizeX/2, e.pos[1] + sizeY/2]
                    ]
                }
            }
        }
    }
}

function getSvgSizeAndPosOffset(entities, tiles, bboxBorderNWSE) {
    if (entities.length === 0 && tiles.length === 0) {
        return [1, 1];
    }

    const entityBboxes = entities.filter(e => "bbox_size" in e).map(e => e.bbox_size);
    const tilePositions = tiles.map(t => t.pos);
    
    const xValues = [
        ...entityBboxes.flatMap(box_size => box_size.map(point => point[0])), 
        ...tilePositions.map(pos => pos[0]),
    ];
    const yValues = [
        ...entityBboxes.flatMap(box_size => box_size.map(point => point[1])), 
        ...tilePositions.map(pos => pos[1]),
    ];

    // Calculate bounding box from both entity bboxes and tile positions
    const bbox = [
        Math.floor(Math.min(...xValues)), // minX
        Math.floor(Math.min(...yValues)), // minY
        Math.ceil(Math.max(...xValues)), // maxX
        Math.ceil(Math.max(...yValues))  // maxY
    ];

    // Apply border
    bbox[0] -= bboxBorderNWSE[1];
    bbox[1] -= bboxBorderNWSE[0];
    bbox[2] += bboxBorderNWSE[3];
    bbox[3] += bboxBorderNWSE[2];

    const bboxWidth = bbox[2] - bbox[0];
    const bboxHeight = bbox[3] - bbox[1];
    const posOffset = [-bbox[0], -bbox[1]];
    return [bboxWidth, bboxHeight, posOffset];
}

function getCurrentBlueprintEntityCount(currentBlueprint){
    const entityCount = {};
    for (const entity of currentBlueprint.entities) {
      entityCount[entity.name] = (entityCount[entity.name] || 0) + 1;
    }
    for (const tile of currentBlueprint.tiles || []) {
        entityCount[tile.name] = (entityCount[tile.name] || 0) + 1;
    }
    return Object.entries(entityCount).sort((a, b) => b[1] - a[1]);
}

function getSVG(bboxWidth, bboxHeight, backgroundColor = "#dddddd", metadataStr = null, svgWidthInMm = 300, aspectRatio = null) {
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

function preProcessDrawingSettings(settings) {
    function resolveBuildingGenericNames(buildNameList) {
        const buildingNameListWithoutGenericTerms = [];
        for (const name of buildNameList) {
            if (name in buildingGenericTerms) {
                buildingNameListWithoutGenericTerms.push(...buildingGenericTerms[name]);
            } else {
                buildingNameListWithoutGenericTerms.push(name);
            }
        }
        return [...new Set(buildingNameListWithoutGenericTerms)];
    }

    settings = JSON.parse(JSON.stringify(settings)); // Deep copy
    const processed_settings = [];
    for (let [settingName, settingProps] of settings) {
        if (settingProps === undefined) {
            settingProps = {};
        }
        if ("allow" in settingProps) {
            settingProps.allow = resolveBuildingGenericNames(settingProps.allow);
        } else if ("deny" in settingProps) {
            settingProps.deny = resolveBuildingGenericNames(settingProps.deny);
        }
        processed_settings.push([settingName, settingProps]);
    }
    return processed_settings;
}

function drawBlueprint(blueprint, settings, svgWidthInMm = 300, aspectRatio = null) {
    const metadataStr = `<metadata generated_with="https://piebro.github.io/factorio-blueprint-visualizer"><settings>${JSON.stringify(settings)}</settings><blueprint>${blueprint.encodedBlueprintStr}</blueprint></metadata>`;

    settings = preProcessDrawingSettings(settings);
    let background = "none";
    for (const [i, [settingName, svgSettings]] of settings.entries()) {
        if (settingName === "default settings") {
            background = svgSettings.background || background;
            delete svgSettings.background;
            break;
        }
    }
    const dwg = getSVG(blueprint.bboxWidth, blueprint.bboxHeight, background, metadataStr, svgWidthInMm, aspectRatio);
    let currentDefaultSettingProps = {};

    for (let [settingName, settingProps] of settings) {
        settingProps = {...currentDefaultSettingProps, ...settingProps};
        if (settingName === "default settings") {
            // appendGroup(dwg, settingProps);
            currentDefaultSettingProps = settingProps;
            continue;
        } else if (settingName === "bbox") {
            drawEntitiesBbox(dwg, blueprint.entities, blueprint.posOffset, settingProps, "bbox_size");
            continue;
        } else if (settingName === "bbox-selection") {
            drawEntitiesBbox(dwg, blueprint.entities, blueprint.posOffset, settingProps, "bbox_selection_size");
            continue;
        } else if (settingName === "bbox-collision") {
            drawEntitiesBbox(dwg, blueprint.entities, blueprint.posOffset, settingProps, "bbox_collision_size");
            continue;
        } else if (settingName === "tiles") {
            drawTiles(dwg, blueprint.tiles, blueprint.posOffset, settingProps);
            continue;
        }
        if (!(settingName in blueprint.cache)) {
            let lines = null;
            if (settingName === "belts") {
                lines = getLinesBelt(blueprint.entities);
            } else if (settingName === "underground-belts") {
                lines = getLinesUndergroundBelt(blueprint.entities);
            } else if (settingName === "pipes") {
                lines = getLinesPipesOrHeatPipes(blueprint.entities, itemToPipeTargetPositions);
            } else if (settingName === "underground-pipes") {
                lines = getLinesUndergroundPipes(blueprint.entities);
            } else if (settingName === "heat-pipes") {
                lines = getLinesPipesOrHeatPipes(blueprint.entities, itemToHeatTargetPositions);
            } else if (settingName === "inserters") {
                lines = getLinesInserter(blueprint.entities);
            } else if (settingName === "rails") {
                lines = getLinesRails(blueprint.entities);
            } else if (settingName === "power-lines") {
                lines = getLinesWire(blueprint.entities, blueprint.wires, WireType.COPPER_WIRE);
            } else if (settingName === "green-wire-lines") {
                lines = getLinesWire(blueprint.entities, blueprint.wires, WireType.GREEN_WIRE);
            } else if (settingName === "red-wire-lines") {
                lines = getLinesWire(blueprint.entities, blueprint.wires, WireType.RED_WIRE);
            } else {
                continue;
            }
            blueprint.cache[settingName] = lines;
        }
        drawLines(dwg, blueprint.cache[settingName], blueprint.posOffset, settingProps);
    }

    for (let i = 0; i < dwg.groupsToClose; i++) {
        dwg.parts.push('</g>');
    }
    dwg.parts.push('</svg>');
    return dwg.parts.join('');
}

function appendGroup(dwg, svgSetting) {
    dwg.parts.push('<g');
    appendSvgSetting(dwg, svgSetting);
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

function appendSvgSetting(dwg, svgSetting) {
    for (const [key, value] of Object.entries(svgSetting)) {
        if (["allow", "deny", "scale", "rx", "ry"].includes(key)) {
            continue;
        }
        dwg.parts.push(` ${key}="${value}"`);
    }
}

function drawRect(dwg, bbox, posOffset, scale, rx, ry) {
    if (scale !== undefined) {
        // Calculate center point
        const centerX = bbox.reduce((sum, point) => sum + point[0], 0) / 4;
        const centerY = bbox.reduce((sum, point) => sum + point[1], 0) / 4;
        
        // Scale points around center
        bbox = bbox.map(point => [
            centerX + (point[0] - centerX) * scale,
            centerY + (point[1] - centerY) * scale
        ]);
    }

    const minX = Math.min(...bbox.map(point => point[0]));
    const minY = Math.min(...bbox.map(point => point[1]));
    const width = Math.abs(bbox[1][0] - bbox[0][0]);
    const height = Math.abs(bbox[2][1] - bbox[1][1]);

    dwg.parts.push(`<rect x="${minX + posOffset[0]}" y="${minY + posOffset[1]}" width="${width}" height="${height}"`);
    
    if (rx !== undefined) {
        dwg.parts.push(` rx="${rx}"`);
    }
    if (ry !== undefined) {
        dwg.parts.push(` ry="${ry}"`);
    }

    dwg.parts.push('/>');
}

function drawEntitiesBbox(dwg, entities, posOffset, settingProps, bboxType) {
    let bboxEntities;
    if ("allow" in settingProps) {
        bboxEntities = entities.filter(e => settingProps.allow.includes(e.name));
    } else if ("deny" in settingProps) {
        bboxEntities = entities.filter(e => !settingProps.deny.includes(e.name));
    } else {
        bboxEntities = entities;
    }

    appendGroup(dwg, settingProps);
    for (const e of bboxEntities) {
        if (bboxType in e) {
            drawRect(dwg, e[bboxType], posOffset, settingProps.scale, settingProps.rx, settingProps.ry);
        }
    }
    dwg.groupsToClose -= 1;
    dwg.parts.push('</g>');
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

function getLinesUndergroundBelt(entities) {
    const nodesInput = {};
    const nodesOutput = {};
    const beltTypes = {
        "underground-belt": 6,
        "fast-underground-belt": 8,
        "express-underground-belt": 10,
        "turbo-underground-belt": 12
    };

    for (const entityName of Object.keys(beltTypes)) {
        nodesInput[entityName] = {};
        nodesOutput[entityName] = {};
    }

    for (const e of entities) {
        if (e.name in beltTypes) {
            const posKey = `${e.pos[0]},${e.pos[1]}`;
            if (e.type === "input") {
                nodesInput[e.name][posKey] = [e.pos, Math.floor(e.direction / 4)];
            } else {
                nodesOutput[e.name][posKey] = [e.pos, Math.floor(e.direction / 4)];
            }
        }
    }

    const lines = [];
    for (const [entityName, maxLength] of Object.entries(beltTypes)) {
        for (const [pos, dir] of Object.values(nodesInput[entityName])) {
            const offset = DIRECTION_4_TO_OFFSET[dir];
            for (let i = 1; i < maxLength; i++) {
                const targetPos = [
                    pos[0] + i * offset[0],
                    pos[1] + i * offset[1]
                ];
                const targetPosKey = `${targetPos[0]},${targetPos[1]}`;
                if (targetPosKey in nodesOutput[entityName] && nodesOutput[entityName][targetPosKey][1] === dir) {
                    lines.push([pos, targetPos]);
                    break;
                }
            }
        }
    }
    return lines;
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

function getLinesInserter(entities) {
    const lines = [];
    for (const e of entities) {
        if (["bulk-inserter", "burner-inserter", "fast-inserter", "inserter", "long-handed-inserter", "stack-inserter"].includes(e.name)) {
            const dir = Math.floor(e.direction / 4);
            const offset = DIRECTION_4_TO_OFFSET[dir];
            const inserterLength = (e.name === "long-handed-inserter" ? 2 : 1);
            lines.push([
                [e.pos[0] + inserterLength * offset[0], e.pos[1] + inserterLength * offset[1]],
                [e.pos[0] + inserterLength * -offset[0], e.pos[1] + inserterLength * -offset[1]]
            ]);
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

function getLinesWire(entities, wires, wireType) {
    const lines = [];
    for (const [w1, w2, w3, w4] of wires) {
        if (w2 === wireType || w4 === wireType) {
            lines.push([entities[w1-1].pos, entities[w3-1].pos]);
        }
    }
    return lines;
}

function drawTiles(dwg, tiles, posOffset, settingProps) {
    function createTileGrid(tiles) {
        const tileNameToGrid = {};
        const minMaxPos = {}
        for (const tile of tiles) {
            if (!(tile.name in tileNameToGrid)) {
                tileNameToGrid[tile.name] = {};
                minMaxPos[tile.name] = {
                    min: [tile.pos[0], tile.pos[1]],
                    max: [tile.pos[0], tile.pos[1]]
                }
            }
            const key = `${tile.pos[0]},${tile.pos[1]}`;
            tileNameToGrid[tile.name][key] = tile.pos;
            minMaxPos[tile.name].min = [Math.min(minMaxPos[tile.name].min[0], tile.pos[0]), Math.min(minMaxPos[tile.name].min[1], tile.pos[1])];
            minMaxPos[tile.name].max = [Math.max(minMaxPos[tile.name].max[0], tile.pos[0]), Math.max(minMaxPos[tile.name].max[1], tile.pos[1])];
        }
    
        const tileNameToGridArrayAndOffset = {};
        for (const [tileName, gridObject] of Object.entries(tileNameToGrid)) {
            const minPos = minMaxPos[tileName].min;
            const maxPos = minMaxPos[tileName].max;
            const width = (maxPos[0] - minPos[0]) + 1 + 4; // +4 for border
            const height = (maxPos[1] - minPos[1]) + 1 + 4
            
            // Create 2D array initialized with false
            const gridArray = []
            for (let x = 0; x < width; x++) {
                gridArray[x] = new Array(height).fill(false);
            }
    
            // Fill in true values for existing tiles
            for (const tile of Object.values(gridObject)) {
                const x = tile[0] - minPos[0];
                const y = tile[1] - minPos[1];
                gridArray[x+2][y+2] = true;
            }
    
            const offset = [minPos[0] - 2, minPos[1] - 2];
            tileNameToGridArrayAndOffset[tileName] = [gridArray, offset];
        }
    
        return tileNameToGridArrayAndOffset;
    }

    function findBorderSegments(gridArray, offset, size) {
        const d = 0.5-size/2
        // 1 => 0 and 0 => 0.5 
        const h = 0.5
        const lines = [];
    
        // Iterate through grid array, skipping border cells
        for (let x = 1; x < gridArray.length - 1; x++) {
            for (let y = 1; y < gridArray[x].length - 1; y++) {
                if (gridArray[x][y]) {
                    continue
                }
                
                const top_middle = gridArray[x][y-1]
                const middle_left = gridArray[x-1][y]
                const middle_right = gridArray[x+1][y]
                const bottom_middle = gridArray[x][y+1]
                
                if (top_middle) {
                    if (middle_right) {
                        if (bottom_middle) {
                            if (middle_left) {
                                // top_middle, middle_right, bottom_middle, middle_left
                                lines.push([[x-d, y-d], [x+d, y-d], [x+d, y+d], [x-d, y+d], [x-d, y-d]]);
                            } else {
                                // top_middle, middle_right, bottom_middle
                                lines.push([[x-h, y+d], [x+d, y+d]]);
                                lines.push([[x+d, y+d], [x+d, y-d]]);
                                lines.push([[x+d, y-d], [x-h, y-d]]);
                            }
                        } else {
                            if (middle_left) {
                                // top_middle, middle_right, middle_left
                                lines.push([[x-d, y+h], [x-d, y-d]]);
                                lines.push([[x-d, y-d], [x+d, y-d]]);
                                lines.push([[x+d, y-d], [x+d, y+h]]);
                            } else {
                                // top_middle, middle_right
                                lines.push([[x-h, y-d], [x+d, y+h]]);
                            }
                        }
                    } else {
                        if (bottom_middle) {
                            if (middle_left) {
                                // top_middle, bottom_middle, middle_left
                                lines.push([[x+h, y+d], [x-d, y+d]]);
                                lines.push([[x-d, y+d], [x-d, y-d]]);
                                lines.push([[x-d, y-d], [x+h, y-d]]);
                            } else {
                                // top_middle, bottom_middle
                                lines.push([[x-h, y-d], [x+h, y-d]]);
                                lines.push([[x-h, y+d], [x+h, y+d]]);
                            }
                        } else {
                            if (middle_left) {
                                // top_middle, middle_left
                                lines.push([[x-d, y+h], [x+h, y-d]]);
                            } else {
                                // top_middle
                                lines.push([[x-h, y-d], [x+h, y-d]]);
                                
                            }
                        }
                    }
                } else {
                    if (middle_right) {
                        if (bottom_middle) {
                            if (middle_left) {
                                // middle_right, bottom_middle, middle_left
                                lines.push([[x-d, y-h], [x-d, y+d]]);
                                lines.push([[x-d, y+d], [x+d, y+d]]);
                                lines.push([[x+d, y+d], [x+d, y-h]]);
                            } else {
                                // middle_right, bottom_middle
                                lines.push([[x-h, y+d], [x+d, y-h]]);
                            }
                        } else {
                            if (middle_left) {
                                // middle_right, middle_left
                                lines.push([[x-d, y-h], [x-d, y+h]]);
                                lines.push([[x+d, y-h], [x+d, y+h]]);
                            } else {
                                // middle_right
                                lines.push([[x+d, y-h], [x+d, y+h]]);
                            }
                        }
                    } else {
                        if (bottom_middle) {
                            if (middle_left) {
                                // bottom_middle, middle_left
                                lines.push([[x-d, y-h], [x+h, y+d]]);
                            } else {
                                // bottom_middle
                                lines.push([[x+h, y+d], [x-h, y+d]]);
                            }
                        } else {
                            if (middle_left) {
                                // middle_left
                                lines.push([[x-d, y-h], [x-d, y+h]]);
                            } else {
                                // -
                            }
                        }
                    }
                }
    
                // look at the corners now
                const top_left = gridArray[x-1][y-1]
                const top_right = gridArray[x+1][y-1]
                const bottom_left = gridArray[x-1][y+1]
                const bottom_right = gridArray[x+1][y+1]
    
                if (top_left && !top_middle && !middle_left) {
                    lines.push([[x-h, y-d], [x-d, y-h]]);
                }
                if (top_right && !top_middle && !middle_right) {
                    lines.push([[x+d, y-h], [x+h, y-d]]);
                }
                if (bottom_left && !bottom_middle && !middle_left) {
                    lines.push([[x-h, y+d], [x-d, y+h]]);
                }
                if (bottom_right && !bottom_middle && !middle_right) {
                    lines.push([[x+h, y+d], [x+d, y+h]]);
                }
            }
        }
    
        lines.forEach(line => line.forEach(point => { point[0] += offset[0]; point[1] += offset[1]; }));
        
        return lines;
    }
    
    function extractPolygons(lines) {
        const rawPolygons = [];
        const connections = new Map();
        
        // Build the connection map (storing all possible connections for each point)
        lines.forEach(line => {
            const [x1, y1] = line[0];
            const [x2, y2] = line[1];
            const point1 = `${x1},${y1}`;
            const point2 = `${x2},${y2}`;
            
            // Add both directions for each connection
            if (!connections.has(point1)) connections.set(point1, new Set());
            if (!connections.has(point2)) connections.set(point2, new Set());
            connections.get(point1).add(point2);
            connections.get(point2).add(point1);
        });
    
        const usedConnections = new Set();
    
        // Process each point that has connections
        for (const startPoint of connections.keys()) {
            // Skip if all connections from this point have been used
            if ([...connections.get(startPoint)].every(endPoint => 
                usedConnections.has(`${startPoint}-${endPoint}`))) continue;
    
            // Start a new polygon
            const polygon = [];
            let currentPoint = startPoint;
            let firstPoint = startPoint;
    
            while (true) {
                // Add the current point to the polygon
                const [x, y] = currentPoint.split(',').map(Number);
                polygon.push([x, y]);
    
                // Find an unused connection from the current point
                const possibleConnections = connections.get(currentPoint);
                const nextPoint = [...possibleConnections].find(endPoint => 
                    !usedConnections.has(`${currentPoint}-${endPoint}`));
    
                if (!nextPoint || (nextPoint === firstPoint && polygon.length > 1)) {
                    // If we've reached the starting point or a dead end
                    if (nextPoint === firstPoint && polygon.length > 2) {
                        rawPolygons.push(polygon);
                    }
                    break;
                }
    
                // Mark this connection as used (in both directions)
                usedConnections.add(`${currentPoint}-${nextPoint}`);
                usedConnections.add(`${nextPoint}-${currentPoint}`);
    
                // Move to the next point
                currentPoint = nextPoint;
            }
        }
        return rawPolygons;
    }
    
    function organizePolygonHierarchy(rawPolygons) {
        function isPointInPolygon(point, polygon) {
            let inside = false;
            for (let i = 0, j = polygon.length - 2; i < polygon.length - 1; j = i++) {
                const xi = polygon[i][0], yi = polygon[i][1];
                const xj = polygon[j][0], yj = polygon[j][1];
                
                const intersect = ((yi > point[1]) !== (yj > point[1]))
                    && (point[0] < (xj - xi) * (point[1] - yi) / (yj - yi) + xi);
                if (intersect) inside = !inside;
            }
            return inside;
        }
        
        function containsPolygon(polyA, polyB) {
            // Use any point from B to test if it's inside A
            const testPoint = polyB[0];
            return isPointInPolygon(testPoint, polyA);
        }
    
        const result = [];
        const used = new Set();
    
        for (let i = 0; i < rawPolygons.length; i++) {
            if (used.has(i)) continue;
    
            const currentPoly = rawPolygons[i];
            const holes = [];
    
            // Find all polygons that are directly contained by this polygon
            for (let j = 0; j < rawPolygons.length; j++) {
                if (i === j || used.has(j)) continue;
    
                if (containsPolygon(currentPoly, rawPolygons[j])) {
                    // Check if this is a direct hole (not contained by any other hole)
                    let isDirectHole = true;
                    for (let k = 0; k < rawPolygons.length; k++) {
                        if (k === i || k === j) continue;
                        if (containsPolygon(rawPolygons[k], rawPolygons[j]) && 
                            containsPolygon(currentPoly, rawPolygons[k])) {
                            isDirectHole = false;
                            break;
                        }
                    }
                    if (isDirectHole) {
                        holes.push(rawPolygons[j]);
                        used.add(j);
                    }
                }
            }
    
            result.push({
                outer: currentPoly,
                holes: holes
            });
            used.add(i);
        }
        return result;
    }
    
    function drawPolygonWithHoles(dwg, polygonHierarchies, posOffset, settingProps) {
        dwg.parts.push('<g');
        appendSvgSetting(dwg, settingProps);
        dwg.parts.push('>');
    
        // For each polygon with its holes
        for (const {outer, holes} of polygonHierarchies) {
            dwg.parts.push('<path fill-rule="evenodd"');
            
            // Start with the outer polygon
            let pathData = 'M ' + outer.map(point => 
                `${point[0] + posOffset[0]},${point[1] + posOffset[1]}`
            ).join(' L ');
            pathData += ' Z';
    
            // Add each hole
            for (const hole of holes) {
                pathData += ' M ' + hole.map(point =>
                    `${point[0] + posOffset[0]},${point[1] + posOffset[1]}`
                ).join(' L ');
                pathData += ' Z';
            }
    
            dwg.parts.push(` d="${pathData}"`);
            dwg.parts.push('/>');
        }
        
        dwg.parts.push('</g>');
    }

    const tileNameToGridArrayAndOffset = createTileGrid(tiles);

    for (const tileName of artificialTilesSortedByLayer) {
        if (!(tileName in tileNameToGridArrayAndOffset)) {
            continue;
        }
        if ("allow" in settingProps && !settingProps.allow.includes(tileName)) {
            continue;
        }
        if ("deny" in settingProps && settingProps.deny.includes(tileName)) {
            continue;
        }
        const [gridArray, offset] = tileNameToGridArrayAndOffset[tileName];
        const scale = "scale" in settingProps ? settingProps.scale : 0.6;
        const lines = findBorderSegments(gridArray, offset, scale);
        const rawPolygons = extractPolygons(lines);
        const result = organizePolygonHierarchy(rawPolygons);
        drawPolygonWithHoles(dwg, result, posOffset, settingProps);
        // debugginDrawLines(dwg, lines, posOffset, { "fill": "none", "stroke": "#ff0000", "stroke-width": 0.1 });
    }
}

function debugginDrawLines(dwg, lines, posOffset, svgSettings) {
    for (const line of lines) {
        dwg.parts.push('<path');
        appendSvgSetting(dwg, svgSettings);
        dwg.parts.push(` d="M${line[0][0] + posOffset[0]} ${line[0][1] + posOffset[1]}`);
        for (const p of line.slice(1)) {
            dwg.parts.push(` L${p[0] + posOffset[0]} ${p[1] + posOffset[1]}`);
        }
        dwg.parts.push('"/>');
    }
}




