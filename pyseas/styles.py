from matplotlib import pyplot as _plt
from matplotlib import rcsetup as _rcsetup
from . import colors as _colors
from . import cm as _cm
from cycler import cycler
from matplotlib.colors import to_rgba


_track_colors = ('#00C1E7,#F59E84,#CC3A8E,#99C945,#DAA51B,#24796C,'
                 '#764E9F,#CA7400,#5D69B1,#BE2045,#58E8C6,#A5AA99').split(',')

_track_cycler = cycler(color=_track_colors)
_artist_cycler = cycler(edgecolor=_track_colors, facecolor=['']*len(_track_colors))
del cycler, _track_colors


_nonfishprops = dict(edgecolor='#AAAAAA', facecolor='none', linewidth=0.6, alpha=0.8)
_fishprops = dict(edgecolor='#DD2222', facecolor='none', linewidth=0.6, alpha=0.8)
_fishing_props = {
    (True, False) : _nonfishprops,
    (False, True) : _nonfishprops,
    (False, False) : _nonfishprops,
    (True, True) : _fishprops,
}
_nonfishprops = dict(color=to_rgba('#AAAAAA'), linewidth=0.6, alpha=0.8)
_fishprops = dict(color=to_rgba('#DD2222'), linewidth=0.6, alpha=0.8)
_linefishing_props = {
    (True, False) : _nonfishprops,
    (False, True) : _nonfishprops,
    (False, False) : _nonfishprops,
    (True, True) : _fishprops,
}
del _nonfishprops, _fishprops


# TODO: add gfw.colormap.family : cm.light / cm.dark
# TODO: then one can pass cmap='fishing' or 'presence' as strings and pick up light or 
# TODO: dark as appropriate

dark = {
        'axes.prop_cycle' : _track_cycler,
        'font.family' : 'Roboto', 
        'font.weight' : 'medium',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'figure.titleweight' : 'medium',
         'text.color' : _colors.dark.title,
         'gfw.fig.background' : _colors.dark.background,
         'gfw.land.color' : _colors.dark.land,
         'gfw.border.color' : _colors.dark.border,
         'gfw.border.linewidth' : 0.4,
         'gfw.ocean.color' : _colors.dark.ocean,
         'gfw.eez.bordercolor' : _colors.dark.eez,
         'gfw.eez.linewidth' : 0.4,
         'gfw.map.centrallongitude' : 0,
         'gfw.map.cmapsrc' : _cm.dark,
         'gfw.map.trackprops' : _artist_cycler,
         'gfw.map.fishingprops' : _fishing_props,
         'gfw.plot.fishingprops' : _linefishing_props}

light = {'axes.prop_cycle' : _track_cycler,
         'font.family' : 'Roboto', 
         'font.weight' : 'normal',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'figure.titleweight' : 'medium',
         'text.color' : _colors.light.title,
         'gfw.fig.background' : _colors.light.background,
         'gfw.land.color' : _colors.light.land,
         'gfw.border.color' : _colors.light.border,
         'gfw.border.linewidth' : 0.4,
         'gfw.ocean.color' : _colors.light.ocean,
         'gfw.eez.bordercolor' : _colors.light.eez,
         'gfw.eez.linewidth' : 0.4,
         'gfw.map.centrallongitude' : 0,
         'gfw.map.cmapsrc' : _cm.light,
         'gfw.map.trackprops' : _artist_cycler,
         'gfw.map.fishingprops' : _fishing_props,
         'gfw.plot.fishingprops' : _linefishing_props}


for k in dark:
    if k.startswith('gfw.'):
        # TODO: add validation
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = dark[k]
del k

