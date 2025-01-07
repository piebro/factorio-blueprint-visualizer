# Factorio Blueprint Visualizer
<p align="center">
    <img src="example_svgs/example_08.svg" width="70%">
</p>

I love the game Factorio and I really like the look of factories after growing for many hours or blueprints after tweaking them for perfection. So I thought about visualizing the factories and blueprints.

All factorio buildings and tiles with their bounding boxes and belt, pipe, rail, inserter, wire and electricity connections can be visualized. Everything is drawn in vector graphics (SVG) to be able to view it in any resolution.

Use the [online demo](https://piebro.github.io/factorio-blueprint-visualizer/) to visualize your own blueprints. With the latest update, Blueprints from Factorio before version 2.0 might not work correctly. You can import older blueprints to factorio and export them again to update them.

## Examples

<p align="center">
<img src="example_svgs/random_0077.svg" width="47%" style="padding: 1% 1% 1% 1%">
<img src="example_svgs/example_06.svg" width="47%" style="padding: 1% 1% 1% 1%">
<img src="example_svgs/example_12.svg" width="47%" style="padding: 1% 1% 1% 1%">
<img src="example_svgs/example_23.svg" width="47%" style="padding: 1% 1% 1% 1%">
<img src="example_svgs/example_24.svg" width="47%" style="padding: 1% 1% 1% 1%">
<img src="example_svgs/example_21.svg" width="47%" style="padding: 1% 1% 1% 1%">
</p>

The last three blueprints are by Josh Ventura and can be found [here](https://factorioprints.com/user/6QrnfqXIffQcWgHC6Xs4uHv1BGg2).

## Updates <!-- TODO add date -->

- Factorio 2.0 and Factorio: Space Age are supported. <!-- TODO: test if I can past older blueprint in factotio 2.0 and export them again to update them -->
- Portet everything to Javascript for simplicity and performance.
- Added ability to modify drawing settings.

## Usage

<!-- TODO: add a few screenshots to visualize a new blueprint? or some text how this generally works? -->
<!-- add link to draw_setting_documenation.md -->

### Text to Image

I created a [dataset](https://huggingface.co/datasets/piebro/factorio-blueprint-visualizations) with images generated using this tool to finetune [SDXL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) (a text-to-image neural network). The model with examples can be found here: https://huggingface.co/piebro/factorio-blueprint-visualizations-sdxl-lora

### Pen Plotting

I have a pen plotter, and one of my initial ideas was also to be able to plot my factories. You can create visualizations you can easily draw. I recommend using https://github.com/abey79/vpype for merging lines together before plotting. An example of a visualization for plotting is here:

<p align="center">
    <img src="example_svgs/example_25.svg" width="70%" style="padding: 1% 1% 1% 1%">
</p>

Another way to create plots from your factories is to use: https://github.com/drawscape-labs/factorio-cli.

### verilog2factorio

It's possible to use https://github.com/redcrafter/verilog2factorio to create factorio verilog blueprints and visualize the buildings and wire connections like this.

<p align="center">
    <img src="example_svgs/example_19.svg" width="20%" style="padding: 1% 1% 1% 1%;">
</p>

### Convert to PNGs

To easily convert all SVGs in a folder, you can use a terminal and Inkscape like this.
```mkdir pngs; for f in *.svg; do inkscape -w 1000 "$f" -e "pngs/${f::-3}png"; done```

## Contribute

```bash
# install uv
uv run ruff check --fix
uv run ruff format
```

Contributions to this project are welcome. Feel free to report bugs or post ideas.

To update the python code for the website, you have to update the python wheel in the website folder. To update it, just run: ```python setup.py bdist_wheel --universal --dist-dir=website```

To update the installed version while developing you can use ```python setup.py bdist_wheel --universal --dist-dir=website && pip uninstall factorioBlueprintVisualizer -y && pip install website/factorioBlueprintVisualizer-1.1.0-py2.py3-none-any.whl```

If you use an external api on localhost (e.g. for getting the blueprint from factorio.school) you need to disable CORS. To start Chrome on Ubuntu with CORS disable you can use ```google-chrome --disable-web-security --user-data-dir=temp http://0.0.0.0:8000/```.

## Statistics

There is lightweight tracking with [Plausible](https://plausible.io/about) for the [website](https://piebro.github.io/factorio-blueprint-visualizer/) to get infos about how many people are visiting. Everyone who is interested can look at these stats here: https://plausible.io/piebro.github.io%2Ffactorio-blueprint-visualizer?period=all