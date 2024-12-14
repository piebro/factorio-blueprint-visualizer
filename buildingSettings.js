// Direction constants
const NORTH = 0;
// const NORTH_EAST = 1;
const EAST = 1;
// const SOUTH_EAST = 3;
const SOUTH = 2;
// const SOUTH_WEST = 5;
const WEST = 3;
// const NORTH_WEST = 7;

// get bbox of all the rail stuff

// const entityNameToProperties = {
//     "wooden-chest": { size: [1,1], genericTerms: ["chests"] },
//     "iron-chest": { size: [1,1], genericTerms: ["chests"] },
//     "steel-chest": { size: [1,1], genericTerms: ["chests"] },
//     "storage-tank": { 
//         size: [3,3], 
//         genericTerms: [],
//         pipe_connection_target_positions: [[0, -2], [0, 2]]
//     },

//     "transport-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "fast-transport-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "express-transport-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "turbo-transport-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "underground-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "fast-underground-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "express-underground-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "turbo-underground-belt": { size: [1,1], genericTerms: ["belts", "transportation"] },
//     "splitter": { size: [2,1], genericTerms: ["belts", "transportation"] },
//     "fast-splitter": { size: [2,1], genericTerms: ["belts", "transportation"] },
//     "express-splitter": { size: [2,1], genericTerms: ["belts", "transportation"] },
//     "turbo-splitter": { size: [2,1], genericTerms: ["belts", "transportation"] },
//     "burner-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "long-handed-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "fast-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "filter-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "stack-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },
//     "stack-filter-inserter": { size: [1,1], genericTerms: ["inserters", "transportation"] },

//     "small-electric-pole": { size: [1,1], genericTerms: ["electricity"] },
//     "medium-electric-pole": { size: [1,1], genericTerms: ["electricity"] },
//     "big-electric-pole": { size: [2,2], genericTerms: ["electricity"] },
//     "substation": { size: [2,2], genericTerms: ["electricity"] },
//     "pipe": {
//         size: [1,1],
//         genericTerms: ["transportation"],
//         pipeConnection: [
//             { pos: [0,0], direction: NORTH },
//             { pos: [0,0], direction: EAST },
//             { pos: [0,0], direction: SOUTH },
//             { pos: [0,0], direction: WEST }
//         ]
//     },
//     "pipe-to-ground": { 
//         size: [1,1], 
//         genericTerms: ["transportation"], 
//         pipeConnection: [{ pos: [0,0], direction: NORTH }]
//     },
//     "pump": { 
//         size: [1,2], 
//         genericTerms: ["transportation"], 
//         pipeConnection: [
//             { pos: [0,0.5], direction: SOUTH },
//             { pos: [0,-0.5], direction: NORTH }
//         ]
//     },

//     "straight-rail": { size: [2,2], genericTerms: ["rails", "ground_rails", "transportation"] },
//     "half-diagonal-rail": { size: [2,2], genericTerms: ["rails", "ground_rails", "transportation"] },
//     "curved-rail-a": { size: [2,2], genericTerms: ["rails", "ground_rails", "transportation"] },
//     "curved-rail-b": { size: [2,2], genericTerms: ["rails", "ground_rails", "transportation"] },

//     "rail-ramp": { size: [4,16], genericTerms: ["rails", "elevated_rails", "transportation"] },
//     "rail-support": { size: [4,4], genericTerms: ["rails", "elevated_rails", "transportation"] },

//     "elevated-straight-rail": { size: [2,2], genericTerms: ["rails", "elevated_rails", "transportation"] },
//     "elevated-half-diagonal-rail": { size: [2,2], genericTerms: ["rails", "elevated_rails", "transportation"] },
//     "elevated-curved-rail-a": { size: [2,2], genericTerms: ["rails", "elevated_rails", "transportation"] },
//     "elevated-curved-rail-b": { size: [2,2], genericTerms: ["rails", "elevated_rails", "transportation"] },

//     "train-stop": { size: [2,2], genericTerms: ["rails"] },
//     "rail-signal": { size: [1,1], genericTerms: ["rails"] },
//     "rail-chain-signal": { size: [1,1], genericTerms: ["rails"] },

//     "logistic-chest-active-provider": { size: [1,1], genericTerms: ["chests", "logistic_chests"] },
//     "logistic-chest-passive-provider": { size: [1,1], genericTerms: ["chests", "logistic_chests"] },
//     "logistic-chest-storage": { size: [1,1], genericTerms: ["chests", "logistic_chests"] },
//     "logistic-chest-buffer": { size: [1,1], genericTerms: ["chests", "logistic_chests"] },
//     "logistic-chest-requester": { size: [1,1], genericTerms: ["chests", "logistic_chests"] },
//     "roboport": { size: [4,4], genericTerms: [] },

//     "small-lamp": { size: [1,1], genericTerms: [] },
//     "arithmetic-combinator": { size: [1,2], genericTerms: ["programming"] },
//     "decider-combinator": { size: [1,2], genericTerms: ["programming"] },
//     "constant-combinator": { size: [1,1], genericTerms: ["programming"] },
//     "power-switch": { size: [2,2], genericTerms: ["programming"] },
//     "programmable-speaker": { size: [1,1], genericTerms: ["programming"] },

//     "boiler": { 
//         size: [3,2], 
//         genericTerms: [], 
//         pipeConnection: [
//             { pos: [0,-0.5], direction: NORTH },
//             { pos: [1,0.5], direction: EAST },
//             { pos: [-1,0.5], direction: WEST }
//         ]
//     },
//     "steam-engine": { 
//         size: [3,5], 
//         genericTerms: ["electricity-generators"],
//         pipeConnection: [
//             { pos: [0,-2], direction: NORTH },
//             { pos: [0,2], direction: SOUTH }
//         ]
//     },
//     "solar-panel": { size: [3,3], genericTerms: ["electricity-generators"] },
//     "accumulator": { size: [2,2], genericTerms: [] },
//     "nuclear-reactor": { size: [5,5], genericTerms: ["nuclear"] },
//     "heat-pipe": {size: [1,1], genericTerms: ["nuclear"] },
//     "heat-exchanger": {
//         size: [3,2],
//         genericTerms: ["nuclear"],
//         pipeConnection: [
//             { pos: [0,-0.5], direction: NORTH },
//             { pos: [1,0.5], direction: EAST },
//             { pos: [-1,0.5], direction: WEST }
//         ]
//     },
//     "steam-turbine": {
//         size: [3,5],
//         genericTerms: ["electricity-generators"],
//         pipeConnection: [
//             { pos: [0,-2], direction: NORTH },
//             { pos: [0,2], direction: SOUTH }
//         ]
//     },

//     "burner-mining-drill": { size: [2,2], genericTerms: ["drills"] },
//     "electric-mining-drill": { size: [3,3], genericTerms: ["drills"] },
//     "offshore-pump": { 
//         size: [1,2], 
//         genericTerms: [], 
//         pipeConnection: [{ pos: [0,0.5], direction: SOUTH }]
//     },
//     "pumpjack": {
//         size: [3,3],
//         genericTerms: ["drills"],
//         pipeConnection: [
//             { pos: [1,-1], direction: NORTH },
//         ]
//     },

//     "stone-furnace": { size: [2,2], genericTerms: ["furnaces"] },
//     "steel-furnace": { size: [2,2], genericTerms: ["furnaces"] },
//     "electric-furnace": { size: [3,3], genericTerms: ["furnaces"] },

//     "assembling-machine-1": { 
//         size: [3,3], 
//         genericTerms: ["assembling-machines", "producing-machines"],
//         pipeConnection: [{ pos: [0,-1], direction: NORTH }]
//     },
//     "assembling-machine-2": { 
//         size: [3,3], 
//         genericTerms: ["assembling-machines", "producing-machines"],
//         pipeConnection: [{ pos: [0,-1], direction: NORTH }]
//     },
//     "assembling-machine-3": { 
//         size: [3,3], 
//         genericTerms: ["assembling-machines", "producing-machines"],
//         pipeConnection: [{ pos: [0,-1], direction: NORTH }]
//     },
//     "oil-refinery": {
//         size: [5,5],
//         genericTerms: ["producing-machines"],
//         pipeConnection: [
//             { pos: [-2,-2], direction: NORTH },
//             { pos: [0,-2], direction: NORTH },
//             { pos: [2,-2], direction: NORTH },
//             { pos: [-1,2], direction: SOUTH },
//             { pos: [1,2], direction: SOUTH }
//         ]
//     },
//     "chemical-plant": {
//         size: [3,3],
//         genericTerms: ["producing-machines"],
//         pipeConnection: [
//             { pos: [-1,-1], direction: NORTH },
//             { pos: [1,-1], direction: NORTH },
//             { pos: [-1,1], direction: SOUTH },
//             { pos: [1,1], direction: SOUTH }
//         ]
//     },
//     "centrifuge": { size: [3,3], genericTerms: ["producing-machines"] },
//     "lab": { size: [3,3], genericTerms: ["science"] },

//     "beacon": { size: [3,3], genericTerms: [] },
//     "rocket-silo": { size: [9,9], genericTerms: ["science"] },

//     "stone-wall": { size: [1,1], genericTerms: ["military"] },
//     "gate": { size: [1,1], genericTerms: ["military"] },
//     "gun-turret": { size: [2,2], genericTerms: ["military", "turret"] },
//     "laser-turret": { size: [2,2], genericTerms: ["military", "turret"] },
//     "flamethrower-turret": {
//         size: [2,3],
//         genericTerms: ["military", "turret"],
//         pipeConnection: [
//             { pos: [-0.5, 1], direction: WEST },
//             { pos: [0.5, 1], direction: EAST },
//         ]
//     },
//     "artillery-turret": { size: [3,3], genericTerms: ["military", "turret"] },
//     "radar": { size: [3,3], genericTerms: ["military"] },
// };


// Generate BUILDING_PIPE_CONNECTIONS from entityNameToProperties
// const BUILDING_PIPE_CONNECTIONS = Object.fromEntries(
//     Object.entries(entityNameToProperties)
//         .filter(([_, props]) => props.pipeConnectionTargetPositions)
//         .map(([name, props]) => [name, props.pipeConnectionTargetPositions])
// );
// console.log("asdaw", BUILDING_PIPE_CONNECTIONS);

// Generate BUILDING_GENERIC_TERMS from entityNameToProperties
const BUILDING_GENERIC_TERMS = {};
Object.entries(entityNameToProperties).forEach(([name, props]) => {
    if (props.genericTerms) {
        props.genericTerms.forEach(term => {
            if (!BUILDING_GENERIC_TERMS[term]) {
                BUILDING_GENERIC_TERMS[term] = [];
            }
            BUILDING_GENERIC_TERMS[term].push(name);
        });
    }
});

// const ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE = {
//     "electric-engine-unit": NORTH,
//     "express-transport-belt": NORTH,
//     "express-underground-belt": NORTH,
//     "express-splitter": NORTH,
//     "rocket-fuel": NORTH,
//     "processing-unit": NORTH,
//     "fill-crude-oil-barrel": NORTH,
//     "empty-crude-oil-barrel": SOUTH,
//     "fill-heavy-oil-barrel": NORTH,
//     "empty-heavy-oil-barrel": SOUTH,
//     "fill-light-oil-barrel": NORTH,
//     "empty-light-oil-barrel": SOUTH,
//     "fill-lubricant-barrel": NORTH,
//     "empty-lubricant-barrel": SOUTH,
//     "fill-petroleum-gas-barrel": NORTH,
//     "empty-petroleum-gas-barrel": SOUTH,
//     "fill-sulfuric-acid-barrel": NORTH,
//     "empty-sulfuric-acid-barrel": SOUTH,
//     "fill-water-barrel": NORTH,
//     "empty-water-barrel": SOUTH,
// };