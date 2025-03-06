from pathlib import Path
from matplotlib import font_manager
from .. import load_fonts  # noqa: F401


data = Path(__file__).parents[1] / "data"

font_dirs = [x for x in (data / "fonts").iterdir() if x.is_dir()]
for font_file in font_manager.findSystemFonts(fontpaths=font_dirs):
    font_manager.fontManager.addfont(font_file)

"""
This chart style was developed on a 10 by 6 figure size. 
Fonts will likely need to be changed for different image sizes.

The chart style is a light theme but could create a dark version in the future.
"""
light = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Roboto", "Arial"],
    "figure.facecolor": "#FFFFFF",
    ### Axes
    "axes.grid": True,  # Turns on grid
    "axes.axisbelow": True,  # Makes grid go behind data
    "grid.color": "#E6E7EB",
    "axes.facecolor": "#FFFFFF",
    "axes.labelweight": "bold",
    "axes.labelsize": 14,
    "axes.labelcolor": "#848B9B",
    "xtick.color": "#848B9B",
    "xtick.labelsize": 12,
    "ytick.color": "#848B9B",
    "ytick.labelsize": 12,
    "axes.spines.right": False,
    "axes.spines.top": False,
    ### Titles/Labels
    "figure.titleweight": "bold",
    "figure.titlesize": 20,
    "text.color": "#363C4C",
    "axes.titleweight": "normal",
    "axes.titlesize": 20,
    "axes.titlecolor": "#363C4C",
    ### Legend
    "legend.fontsize": 14,
    # how to make legend text a 848B9B???
    "figure.subplot.hspace": 0.4,
    ### Plots
    "legend.frameon": False,
}
