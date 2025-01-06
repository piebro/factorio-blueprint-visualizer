# Drawing Settings Documentation

The drawing settings control how your Factorio blueprint is visualized. Settings are defined as an array of arrays, where each inner array represents a drawing instruction.

## Basic Format

```json
[
    ['setting-name', {svg-attributes}, {optional-parameters}]
]
```

Each setting consists of:
1. Setting name (string)
2. SVG attributes object (required, can be empty `{}`)
3. Optional parameters object (optional)

An example can be found in [drawingSettings.js](drawingSettings.js).

## Available Setting Names

- `default settings`: Default settings for the blueprint if some settings are not specified.
- `tiles`: Draws tiles.
- `bbox`: Draws the bounding box of buildings.
- `bbox-selection`: Draws the selection bounding box of buildings.
- `bbox-collision`: Draws the collision bounding box of buildings.
- `pipes`: Draws pipes.
- `underground-pipes`: Draws underground pipes.
- `belts`: Draws belts.
- `underground-belts`: Draws underground belts.
- `heat-pipes`: Draws heat pipes.
- `power-lines`: Draws power lines.
- `green-wire-lines`: Draws green wire lines.
- `red-wire-lines`: Draws red wire lines.

## SVG Attributes

- `fill`: Color for filling shapes
- `fill-opacity`: Transparency of fill (0.0 to 1.0)
- `stroke`: Color for lines/borders
- `stroke-width`: Width of lines/borders
- `stroke-linecap`: Style of line endings ('round', 'butt', 'square')
- `stroke-opacity`: Transparency of lines (0.0 to 1.0)

## Optional Parameters

These parameters can only be used in tiles and bbox settings.

- `allow`: Array of strings, only draw entities that match any of these strings.
- `deny`: Array of strings, do not draw entities that match any of these strings.
- `scale`: Number, scale of the entity.
- `rx`: Number, radius of the rounded corners for rectangles.
- `ry`: Number, radius of the rounded corners for rectangles.

`allow` and `deny` can be used with the name of the entity (e.g. `fast-inserter` or `assembling-machine-1`) or with the generic terms of the entity (e.g. `combat` or `inserter`).
All generic terms can be found in [entityProperties.js](entityProperties.js).

