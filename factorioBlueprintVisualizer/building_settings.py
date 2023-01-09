NORTH = 0
NORTH_EAST = 1
EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7


entity_name_to_properties = {
  # first tab: Logistics
  "wooden-chest": {"size":(1,1), "generic_terms": ["chests"]},
  "iron-chest": {"size":(1,1), "generic_terms": ["chests"]},
  "steel-chest": {"size":(1,1), "generic_terms": ["chests"]},
  "storage-tank": {"size":(3,3), "generic_terms": []},

  "transport-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "fast-transport-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "express-transport-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "underground-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "fast-underground-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "express-underground-belt": {"size":(1,1), "generic_terms": ["belts", "transportation"]},
  "splitter": {"size":(2,1), "generic_terms": ["belts", "transportation"]},
  "fast-splitter": {"size":(2,1), "generic_terms": ["belts", "transportation"]},
  "express-splitter": {"size":(2,1), "generic_terms": ["belts", "transportation"]},

  "burner-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "long-handed-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "fast-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "filter-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "stack-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},
  "stack-filter-inserter": {"size":(1,1), "generic_terms": ["inserters", "transportation"]},

  "small-electric-pole": {"size":(1,1), "generic_terms": ["electricity"]},
  "medium-electric-pole": {"size":(1,1), "generic_terms": ["electricity"]},
  "big-electric-pole": {"size":(2,2), "generic_terms": ["electricity"]},
  "substation": {"size":(2,2), "generic_terms": ["electricity"]},
  "pipe": {
    "size":(1,1),
    "generic_terms": ["transportation"],
    "pipe_connection": [{"pos":(0,0), "direction": NORTH}, {"pos":(0,0), "direction": EAST}, {"pos":(0,0), "direction": SOUTH}, {"pos":(0,0), "direction": WEST}]
  },
  "pipe-to-ground": {"size":(1,1), "generic_terms": ["transportation"], "pipe_connection": [{"pos":(0,0), "direction": NORTH}]},
  "pump": {"size":(1,2), "generic_terms": ["transportation"], "pipe_connection": [{"pos":(0,0.5), "direction": SOUTH}, {"pos":(0,-0.5), "direction": NORTH}]},

  "straight-rail": {"size":(2,2), "generic_terms": ["rails", "transportation"]},
  "curved-rail": {"size":(2,2), "generic_terms": ["rails", "transportation"]},
  "train-stop": {"size":(2,2), "generic_terms": ["rails"]},
  "rail-signal": {"size":(1,1), "generic_terms": ["rails"]},
  "rail-chain-signal": {"size":(1,1), "generic_terms": ["rails"]},

  "logistic-chest-active-provider": {"size":(1,1), "generic_terms": ["chests", "logistic_chests"]},
  "logistic-chest-passive-provider": {"size":(1,1), "generic_terms": ["chests", "logistic_chests"]},
  "logistic-chest-storage": {"size":(1,1), "generic_terms": ["chests", "logistic_chests"]},
  "logistic-chest-buffer": {"size":(1,1), "generic_terms": ["chests", "logistic_chests"]},
  "logistic-chest-requester": {"size":(1,1), "generic_terms": ["chests", "logistic_chests"]},
  "roboport": {"size":(4,4), "generic_terms": []},

  # tab 2
  "small-lamp": {"size":(1,1), "generic_terms": []},
  "arithmetic-combinator": {"size":(1,2), "generic_terms": ["programming"]},
  "decider-combinator": {"size":(1,2), "generic_terms": ["programming"]},
  "constant-combinator": {"size":(1,1), "generic_terms": ["programming"]},
  "power-switch": {"size":(2,2), "generic_terms": ["programming"]},
  "programmable-speaker": {"size":(1,1), "generic_terms": ["programming"]},

  "boiler": {"size":(3,2), "generic_terms": [], "pipe_connection": [{"pos":(0,-0.5), "direction": NORTH}, {"pos":(1,0.5), "direction": EAST}, {"pos":(-1,0.5), "direction": WEST}]},
  "steam-engine": {"size":(3,5), "generic_terms": ["electricity-generators"], "pipe_connection": [{"pos":(0,-2), "direction": NORTH}, {"pos":(0,2), "direction": SOUTH}]},
  "solar-panel": {"size":(3,3), "generic_terms": ["electricity-generators"]},
  "accumulator": {"size":(2,2), "generic_terms": []},
  "nuclear-reactor": {"size":(5,5), "generic_terms": ["nuclear"]},
  "heat-pipe": {"size":(1,1), "generic_terms": ["nuclear"]},
  "heat-exchanger": {"size":(3,2), "generic_terms": ["nuclear"]},
  "steam-turbine": {"size":(3,5), "generic_terms": ["electricity-generators"]},

  "burner-mining-drill": {"size":(2,2), "generic_terms": ["drills"]},
  "electric-mining-drill": {"size":(3,3), "generic_terms": ["drills"]},
  "offshore-pump": {"size":(1,2), "generic_terms": [], "pipe_connection": [{"pos":(0,0.5), "direction": SOUTH}]},
  "pumpjack": {"size":(3,3), "generic_terms": ["drills"]},

  "stone-furnace": {"size":(2,2), "generic_terms": ["furnaces"]},
  "steel-furnace": {"size":(2,2), "generic_terms": ["furnaces"]},
  "electric-furnace": {"size":(3,3), "generic_terms": ["furnaces"]},

  "assembling-machine-1": {"size":(3,3), "generic_terms": ["assembling-machines", "producing-machines"], "pipe_connection": [{"pos":(0,-1), "direction": NORTH}]},
  "assembling-machine-2": {"size":(3,3), "generic_terms": ["assembling-machines", "producing-machines"], "pipe_connection": [{"pos":(0,-1), "direction": NORTH}]},
  "assembling-machine-3": {"size":(3,3), "generic_terms": ["assembling-machines", "producing-machines"], "pipe_connection": [{"pos":(0,-1), "direction": NORTH}]},
  "oil-refinery": {
    "size":(5,5),
    "generic_terms": ["producing-machines"], 
    "pipe_connection": [{"pos":(-2,-2), "direction": NORTH}, {"pos":(0,-2), "direction": NORTH}, {"pos":(2,-2), "direction": NORTH}, {"pos":(-1,2), "direction": SOUTH}, {"pos":(1,2), "direction": SOUTH}]
  },
  "chemical-plant": {
    "size":(3,3),
    "generic_terms": ["producing-machines"],
    "pipe_connection": [{"pos":(-1,-1), "direction": NORTH}, {"pos":(1,-1), "direction": NORTH}, {"pos":(-1,1), "direction": SOUTH}, {"pos":(1,1), "direction": SOUTH}]
  },
  "centrifuge": {"size":(3,3), "generic_terms": ["producing-machines"]},
  "lab": {"size":(3,3), "generic_terms": ["science"]},

  "beacon": {"size":(3,3), "generic_terms": []},
  "rocket-silo": {"size":(9,9), "generic_terms": ["science"]},

  # tab 3
  "stone-wall": {"size":(1,1), "generic_terms": ["military"]},
  "gate": {"size":(1,1), "generic_terms": ["military"]},
  "gun-turret": {"size":(2,2), "generic_terms": ["military", "turret"]},
  "laser-turret": {"size":(2,2), "generic_terms": ["military", "turret"]},
  "flamethrower-turret": {"size":(2,3), "generic_terms": ["military", "turret"]},
  "artillery-turret": {"size":(3,3), "generic_terms": ["military", "turret"]},
  "radar": {"size":(3,3), "generic_terms": ["military"]},

}

BUILDING_SIZES = {name: properties["size"] for name, properties in entity_name_to_properties.items() if "size" in properties}
BUILDING_PIPE_CONNECTIONS = {name: properties["pipe_connection"] for name, properties in entity_name_to_properties.items() if "pipe_connection" in properties}


BUILDING_GENERIC_TERMS = {}
for name, properties in entity_name_to_properties.items():
  if "generic_terms" in properties:
    for generic_term in properties["generic_terms"]:
      if generic_term not in BUILDING_GENERIC_TERMS:
        BUILDING_GENERIC_TERMS[generic_term] = []
      BUILDING_GENERIC_TERMS[generic_term].append(name)


ASSEMBLY_MACHINE_RECIPE_TO_DIR_CHANGE = {
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
