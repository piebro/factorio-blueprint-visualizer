NORTH = 0
NORTH_EAST = 1
EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7

BUILDING_SIZES = {
    # first tab: Logistics
    "wooden-chest": (1,1),
    "iron-chest": (1,1),
    "steel-chest": (1,1),
    "storage-tank": (3,3),

    "transport-belt": (1,1),
    "fast-transport-belt": (1,1),
    "express-transport-belt": (1,1),
    "underground-belt": (1,1),
    "fast-underground-belt": (1,1),
    "express-underground-belt": (1,1),
    "splitter": (2,1),
    "fast-splitter": (2,1),
    "express-splitter": (2,1),

    "burner-inserter": (1,1),
    "inserter": (1,1),
    "long-handed-inserter": (1,1),
    "fast-inserter": (1,1),
    "filter-inserter": (1,1),
    "stack-inserter": (1,1),
    "stack-filter-inserter": (1,1),

    "small-electric-pole": (1,1),
    "medium-electric-pole": (1,1),
    "big-electric-pole": (2,2),
    "substation": (2,2),
    "pipe": (1,1),
    "pipe-to-ground": (1,1),
    "pump": (1,2),

    "straight-rail": (2,2),
    "curved-rail": (2,2),
    "train-stop": (2,2),
    "rail-signal": (1,1),
    "rail-chain-signal": (1,1),

    "logistic-chest-active-provider": (1,1),
    "logistic-chest-passive-provider": (1,1),
    "logistic-chest-storage": (1,1),
    "logistic-chest-buffer": (1,1),
    "logistic-chest-requester": (1,1),
    "roboport": (4,4),

    "small-lamp": (1,1),
    "arithmetic-combinator": (1,2),
    "decider-combinator": (1,2),
    "constant-combinator": (1,1),
    "power-switch": (2,2),
    "programmable-speaker": (1,1),

    # tap 2
    "boiler": (3, 2),
    "steam-engine": (3,5), ####
    "solar-panel": (3,3),
    "accumulator": (2,2),
    "nuclear-reactor": (5,5),
    "heat-pipe": (1,1),
    "heat-exchanger": (3,2),
    "steam-turbine": (3,5),

    "burner-mining-drill": (2,2),
    "electric-mining-drill": (3,3),
    "offshore-pump": (1, 2),
    "pumpjack": (3,3),

    "stone-furnace": (2,2),
    "steel-furnace": (2,2),
    "electric-furnace": (3,3),

    "assembling-machine-1": (3,3),
    "assembling-machine-2": (3,3),
    "assembling-machine-3": (3,3),
    "oil-refinery": (5,5),
    "chemical-plant": (3,3),
    "centrifuge": (3,3),
    "lab": (3,3),

    "beacon": (3,3),
    "rocket-silo": (9,9),

    # tap 3
    "stone-wall": (1,1),
    "gate": (1,1),
    "gun-turret": (2,2),
    "laser-turret": (2,2),
    "flamethrower-turret": (2,3),
    "artillery-turret": (3,3),
    "radar": (3,3),

    ### MODS
    # Factorissimo2
    "factory-1":(8,8),
    "factory-2":(12,12),
    "factory-3":(16,16),
    "factory-circuit-input": (1,1),
    "factory-circuit-output": (1,1),
    "factory-input-pipe": (1,1),
    "factory-output-pipe": (1,1),
    "factory-requester-chest": (1,1),
}

BUILDING_GENERIC_TERMS = {
    "assembling-machine": ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3"],
    "producing-machines": ["assembling-machine-1", "assembling-machine-2", "assembling-machine-3", "oil-refinery",
                           "chemical-plant", "centrifuge"],
    "belt-stuff": ["transport-belt", "fast-transport-belt", "express-transport-belt", "underground-belt",
                   "fast-underground-belt", "express-underground-belt", "splitter", "fast-splitter",
                   "express-splitter"],
    "electric-stuff": ["small-electric-pole", "medium-electric-pole", "big-electric-pole", "substation"],
    "furnace": ["stone-furnace", "steel-furnace", "electric-furnace"],
    "drill": ["burner-mining-drill", "electric-mining-drill", "pumpjack"],
    "electicity-generation": ["steam-engine", "solar-panel", "nuclear-reactor", "steam-turbine"],
    "military": ["stone-wall", "gate", "gun-turret", "laser-turret", "flamethrower-turret", "artillery-turret",
                 "radar"],
    "all-inserter": ["burner-inserter", "inserter", "long-handed-inserter", "fast-inserter", "filter-inserter",
                     "stack-inserter", "stack-filter-inserter"],
    "chests": ["wooden-chest", "iron-chest", "steel-chest", "logistic-chest-active-provider",
               "logistic-chest-passive-provider", "logistic-chest-storage", "logistic-chest-buffer",
               "logistic-chest-requester"],
    "rail": ["straight-rail", "curved-rail"],
    "connected-stuff": ["transport-belt", "fast-transport-belt", "express-transport-belt", "underground-belt",
                  "fast-underground-belt", "express-underground-belt", "splitter", "fast-splitter", "express-splitter",
                  "straight-rail", "curved-rail", "pipe", "pipe-to-ground", "burner-inserter", "inserter",
                  "long-handed-inserter", "fast-inserter", "filter-inserter", "stack-inserter",
                  "stack-filter-inserter"],
    "train-stuff": ["straight-rail", "curved-rail", "train-stop", "rail-signal", "rail-chain-signal"],

    ### MODS
    # Factorissimo2
    "factorissimo2": ["factory-1", "factory-2", "factory-3", "factory-circuit-input", "factory-circuit-output", "factory-input-pipe", "factory-output-pipe", "factory-requester-chest"],
}

RECIPES_IN_ASSEMBLY_MACHINE_WITH_FLUIDS_TO_DIR_CHANGE = {
  "electric-engine-unit": NORTH,
  "express-transport-belt": NORTH,
  "express-underground-belt": NORTH,
  "express-splitter": NORTH,
  "rocket-fuel": NORTH,
  "processing-unit": NORTH,
  "fill-crude-oil-barrel": NORTH,
  "empty-crude-oil-barrel": SOUTH,
  "fill-heavy-oil-barrel": NORTH,
  "empty-heavy-oil-barrel": SOUTH,
  "fill-light-oil-barrel": NORTH,
  "empty-light-oil-barrel": SOUTH,
  "fill-lubricant-barrel": NORTH,
  "empty-lubricant-barrel": SOUTH,
  "fill-petroleum-gas-barrel": NORTH,
  "empty-petroleum-gas-barrel": SOUTH,
  "fill-sulfuric-acid-barrel": NORTH,
  "empty-sulfuric-acid-barrel": SOUTH,
  "fill-water-barrel": NORTH,
  "empty-water-barrel": SOUTH,
}

BUILDING_PIPE_CONNECTIONS = {
    "pipe":[
      {"pos":(0,0), "direction": NORTH},
      {"pos":(0,0), "direction": EAST},
      {"pos":(0,0), "direction": SOUTH},
      {"pos":(0,0), "direction": WEST}      
    ],
    "assembling-machine-1":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "assembling-machine-2":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "assembling-machine-3":[
      {"pos":(0,-1), "direction": NORTH}
    ],
    "boiler":[
      {"pos":(0,-0.5), "direction": NORTH},
      {"pos":(1,0.5), "direction": EAST},
      {"pos":(-1,0.5), "direction": WEST}
    ],
    "pipe-to-ground":[
      {"pos":(0,0), "direction": NORTH}
    ],
    "offshore-pump":[
      {"pos":(0,0.5), "direction": SOUTH}
    ],
    "steam-engine":[
      {"pos":(0,-2), "direction": NORTH},
      {"pos":(0,2), "direction": SOUTH}
    ],
    "oil-refinery":[
      {"pos":(-2,-2), "direction": NORTH},
      {"pos":(0,-2), "direction": NORTH},
      {"pos":(2,-2), "direction": NORTH},
      {"pos":(-1,2), "direction": SOUTH},
      {"pos":(1,2), "direction": SOUTH}
    ],
    "chemical-plant":[
      {"pos":(-1,-1), "direction": NORTH},
      {"pos":(1,-1), "direction": NORTH},
      {"pos":(-1,1), "direction": SOUTH},
      {"pos":(1,1), "direction": SOUTH}
    ],
}

