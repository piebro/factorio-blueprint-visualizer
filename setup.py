from setuptools import setup
from pathlib import Path

parent_dir = Path(__file__).resolve().parent

setup(
    name='factorioBlueprintVisualizer',
    version='1.0.0',
    
    description="A python library to artfully visualize Factorio Blueprints.",
    url="https://github.com/piebro/factorio-blueprint-visualizers",
    author="Piet Brömmel",
    license="MIT License",
    install_requires=parent_dir.joinpath("requirements.txt").read_text().splitlines(),
    packages=['factorioBlueprintVisualizer'],
)