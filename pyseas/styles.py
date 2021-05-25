from cycler import cycler as _cycler, Cycler as _Cycler
from matplotlib import pyplot as _plt
from matplotlib import rcsetup as _rcsetup
from matplotlib import font_manager
import os
from pathlib import Path
from . import props as _props
from . import cm as _cm
from matplotlib.colors import to_rgba
import skimage.io as skio

root = Path(__file__).parents[1]
data = Path(__file__).parents[0] / 'data'

font_dirs = [os.path.join(font_dir_loc, x) for x in (data / 'fonts').iterdir() if x.is_dir()]
for file in font_manager.findSystemFonts(fontpaths=font_dirs):
    font_manager.fontManager.addfont(font_file)

"""
This chart style was developed on a 10 by 6 figure size. 
Fonts will likely need to be changed for different image sizes.

The chart style is a light theme but could create a dark version in the future.
"""
chart_style = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Roboto', 'Arial'],
    'figure.facecolor': '#F7F7F7',

    ### Axes
    'axes.grid': True, #Turns on grid
    'axes.linewidth': 0, #Turns off axis lines
    'axes.axisbelow': True, #Makes grid go behind data
    'grid.color': '#E6E7EB',
    'axes.facecolor': '#F7F7F7',
    'axes.labelweight': 'bold',
    'axes.labelsize': 14,
    'axes.labelcolor': '#848B9B',
    'xtick.color': '#848B9B',
    'xtick.labelsize': 12,
    'ytick.color': '#848B9B',
    'ytick.labelsize': 12,

    ### Titles/Labels
    'figure.titleweight': 'bold',
    'figure.titlesize': 20,
    'text.color': '#363C4C',
    'axes.titleweight': 'normal',
    'axes.titlesize': 20,
    'axes.titlecolor': '#363C4C',

    ### Legend
    'legend.fontsize': 14,
    # how to make legend text a 848B9B???

    'figure.subplot.hspace': 0.4,
}


_light_track_cycler = _cycler(color=_props.light.track.colors)
_light_artist_cycler = _cycler(edgecolor=_props.light.track.colors,
        facecolor=[(0, 0, 0, 0)]*len(_props.light.track.colors))
_dark_track_cycler = _cycler(color=_props.dark.track.colors)
_dark_artist_cycler = _cycler(edgecolor=_props.dark.track.colors,
    facecolor=[(0, 0, 0, 0)]*len(_props.dark.track.colors))

_chart_colors = []
for clr in _props.chart.colors._100_percent:
    _chart_colors.append(clr)

_chart_cycler = _cycler(color=_chart_colors, linewidth=[2]*len(_chart_colors))
del _chart_colors, clr


def create_props(kinds, colors=None, interstitial_color=(0.5, 0.5, 0.5, 1)):
    """Create props suitable for track plots.

    Parameters
    ----------
    kinds : list of str
        The keys for different values in the plot
    colors : list of str or cycler.Cycler, optional
        Colors to apply to line segments. These are paired with `kinds` the values
        supplied above and added to the output dict under `(k, k)`
        If a Cycler, then the cycler should supply `edgecolor` and `facecolor` values (facecolor
        should be transparent). By default, pulls the cycler from trackprops.
    interstitial_color : matplotlib color value, optional
        Color to apply to segments between points with different kind values.

    Returns
    -------
    dict mapping (k1, k2) to props
    """
    if colors is None:
        prop_cycle = _plt.rcParams.get('pyseas.map.trackprops', _dark_artist_cycler)
    elif isinstance(colors, (list, int)):
        prop_cycle = _cycler(edgecolor=colors, facecolor=[(0, 0, 0, 0)] * len(colors))
    elif isinstance(colors, _Cycler):
        prop_cycle = colors
    else:
        raise ValueError(f"don't know how to handle props of type {type(props)}")
    prop_cycle = prop_cycle()
    props = {}
    for k1 in kinds:
        props[(k1, k1)] = next(prop_cycle)
        for k2 in kinds:
            if k1 != k2:
                props[(k1, k2)] = {'edgecolor' : interstitial_color,
                                   'facecolor' : (0, 0, 0, 0),
                                   'legend' : None}
    return props



def create_plot_panel_props(prop_map):
    """Create props suitable for plot panel

    Parameters
    ----------
    prop_map: dict or OrderedDict (Python 2)
        background colors should typically come first

    Returns
    -------
    dict mapping (k1, k2) to props
    """
    props = {}
    for k1, v in prop_map.items():
        v = {'edgecolor' : v.get('color', None),
             'facecolor' : 'none',
             'linewidth' : v.get('width', None),
             'alpha' : v.get('alpha', None)}
        for k2, _ in prop_map.items():
            if (k1, k2) not in props:
                props[k1, k2] = v
            if (k2, k1) not in props:
                props[k2, k1] = v
    return props


_fishing_props = create_plot_panel_props({
    -1 : {'color' : _props.fishing.undefined.color, 'width' : _props.fishing.undefined.width, 
          'alpha' : _props.fishing.undefined.alpha},
     0 : {'color' : _props.fishing.non_fishing.color, 'width' : _props.fishing.non_fishing.width, 
          'alpha' : _props.fishing.non_fishing.alpha},
     1 : {'color' : _props.fishing.fishing.color, 'width' : _props.fishing.fishing.width, 
          'alpha' : _props.fishing.fishing.alpha}
     })


_annotationmapprops = dict(fontdict={'color' : 'black', 'weight': 'bold', 'size' : 10},
                           bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'))

_annotationplotprops = dict(fontdict={'size' : 10, 'weight' : 'medium'})

_colorbarlabelfont  = {'fontsize': 12}


def load_default_logo(name):
    return skio.imread(os.path.join(root, 'pyseas/data/logos', name))


dark = {
        'text.usetex' : False,
        'grid.alpha': _props.dark.grid.alpha,
        'grid.color': _props.dark.grid.color,
        'grid.linestyle': _props.dark.grid.style,
        'grid.linewidth': _props.dark.grid.width,
        'axes.prop_cycle' : _dark_track_cycler,
        'font.family' : _props.dark.font.family, 
        'font.weight' : _props.dark.font.weight,
         'xtick.color' : _props.dark.tick.color,
         'ytick.color' : _props.dark.tick.color,
         'xtick.labelsize' : _props.dark.tick.label_size,
         'ytick.labelsize' : _props.dark.tick.label_size,
         'axes.labelsize' : _props.dark.label.size,
         'axes.labelcolor' : _props.dark.label.color,
         'axes.labelweight' : _props.dark.label.weight,
         'axes.titleweight' : _props.dark.font.weight,
         'figure.titleweight' :_props.dark.font.weight,
         'axes.edgecolor' : _props.dark.frame.color,
         'text.color' : _props.dark.title.color,
         'pyseas.fig.background' : _props.dark.background.color,
         'pyseas.land.color' : _props.dark.land.color,
         'pyseas.border.color' : _props.dark.border.color,
         'pyseas.border.linewidth' : _props.dark.border.width,
         'pyseas.ocean.color' : _props.dark.ocean.color,
         'pyseas.highlight.color' : _props.dark.highlight.color,
         'pyseas.eez.bordercolor' : _props.dark.eez.color,
         'pyseas.eez.linewidth' : _props.dark.eez.width,
         'pyseas.map.cmapsrc' : _cm.dark,
         'pyseas.map.trackprops' : _dark_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : _props.dark.projection_label.size,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo' : load_default_logo(_props.dark.logo.name),
         'pyseas.logo.scale_adj' : _props.dark.scale_adj,
         'pyseas.logo.alpha' : _props.dark.logo.alpha,
         'pyseas.miniglobe.overlaycolor' : _props.dark.miniglobe.overlaycolor,
         'pyseas.miniglobe.outerwidth' : _props.dark.miniglobe.outer_width,
         'pyseas.miniglobe.innerwidth' : _props.dark.miniglobe.inner_width,
         'pyseas.miniglobe.ptsperside' : _props.dark.miniglobe.pts_per_side,
         }

light = {
         'text.usetex' : False,
         'grid.alpha': _props.light.grid.alpha,
         'grid.color': _props.light.grid.color,
         'grid.linestyle': _props.light.grid.style,
         'grid.linewidth': _props.light.grid.width,
         'axes.prop_cycle' : _light_track_cycler,
         'font.family' : _props.light.font.family, 
         'font.weight' : _props.light.font.weight,
         'xtick.color' : _props.light.tick.color,
         'ytick.color' : _props.light.tick.color,
         'xtick.labelsize' : _props.light.tick.label_size,
         'ytick.labelsize' : _props.light.tick.label_size,
         'axes.labelsize' : _props.light.label.size,
         'axes.labelcolor' : _props.light.label.color,
         'axes.labelweight' : _props.light.label.weight,
         'axes.titleweight' : _props.light.font.weight,
         'axes.edgecolor' : _props.light.frame.color,
         'figure.titleweight' : _props.light.font.weight,
         'text.color' : _props.light.title.color,
         'pyseas.fig.background' : _props.light.background.color,
         'pyseas.land.color' : _props.light.land.color,
         'pyseas.border.color' : _props.light.border.color,
         'pyseas.border.linewidth' : _props.light.border.width,
         'pyseas.ocean.color' : _props.light.ocean.color,
         'pyseas.highlight.color' : _props.light.highlight.color,
         'pyseas.eez.bordercolor' : _props.light.eez.color,
         'pyseas.eez.linewidth' : _props.light.eez.width,
         'pyseas.map.cmapsrc' : _cm.light,
         'pyseas.map.trackprops' : _light_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : _props.dark.projection_label.size,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo' : load_default_logo(_props.light.logo.name),
         'pyseas.logo.scale_adj' : _props.light.scale_adj,
         'pyseas.logo.alpha' : _props.light.logo.alpha,
         'pyseas.miniglobe.overlaycolor' : _props.light.miniglobe.overlaycolor,
         'pyseas.miniglobe.outerwidth' : _props.light.miniglobe.outer_width,
         'pyseas.miniglobe.innerwidth' : _props.light.miniglobe.inner_width,
         'pyseas.miniglobe.ptsperside' : _props.light.miniglobe.pts_per_side,
         }

panel = light.copy()
panel.update({
    'pyseas.nightshade.color' : _props.chart.nightshade.color,
    'pyseas.nightshade.alpha' : _props.chart.nightshade.alpha,
})



for k in panel:
    if k.startswith('pyseas.'):
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = panel[k]
del k


def set_default_logos(light_logo=None, dark_logo=None, scale_adj=1, alpha=None):
    """Set the default logos to use with add_logo

    Either the light logo, the dark logo, or both may be specified. If both,
    then scale_adj and alpha applies to both. If neither is specified, nothing
    is done.

    Parameters
    ----------
    light_logo, dark_logo : array, optional
        Must be in a format that matplotlib understands.
    scale_adj : float, optional
        The default image scale is multiplied by this amount.
    alpha : float or None, optional
        Set the image alpha. If not specified, the image alpha is inherited from previous
        logos.
    """
    if light_logo is not None:
        light['pyseas.logo'] = light_logo
        light['pyseas.logo.scale_adj'] = scale_adj
        if alpha is not None:
            light['pyseas.logo.alpha'] = alpha
    if dark_logo is not None:
        dark['pyseas.logo'] = dark_logo
        dark['pyseas.logo.scale_adj'] = scale_adj
        if alpha is not None:
            dark['pyseas.logo.alpha'] = alpha

