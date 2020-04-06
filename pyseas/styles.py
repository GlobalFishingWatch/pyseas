from matplotlib import pyplot as _plt
from matplotlib import rcsetup as _rcsetup
from . import colors as _colors
from . import cm as _cm
from cycler import cycler
from matplotlib.colors import to_rgba


_light_track_cycler = cycler(color=_colors.light.colors)
_light_artist_cycler = cycler(edgecolor=_colors.light.colors, facecolor=[(0, 0, 0, 0)]*len(_colors.light.colors))
_dark_track_cycler = cycler(color=_colors.dark.colors)
_dark_artist_cycler = cycler(edgecolor=_colors.dark.colors, facecolor=[(0, 0, 0, 0)]*len(_colors.dark.colors))

_chart_colors = []
for clr in _colors.chart.colors:
    _chart_colors.append(clr.p100)

_chart_cycler = cycler(color=_chart_colors, linewidth=[2]*len(_chart_colors))
del cycler, _chart_colors, clr


_undef = dict(edgecolor='#888888', facecolor='none', linewidth=0.1, alpha=0.8)
_nonfishprops = dict(edgecolor='#559999', facecolor='none', linewidth=0.6, alpha=0.8)
_fishprops = dict(edgecolor='#DD2222', facecolor='none', linewidth=0.6, alpha=0.8)
_fishing_props = {
    (1, 0) : _nonfishprops,
    (0, 1) : _nonfishprops,
    (0, 0) : _nonfishprops,
    (1, 1) : _fishprops,
    (-1, -1) : _undef,
    (-1, 0) : _undef,
    (-1, 1) : _undef,
    (0, -1) : _undef,
    (1, -1) : _undef,
}

_annotationmapprops = dict(fontdict={'color' : 'black', 'weight': 'bold', 'size' : 10},
                           bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle'))

_annotationplotprops = dict(fontdict={'size' : 10, 'weight' : 'medium'})

_colorbarlabelfont  = {'fontsize': 12}

# TODO: swap 'pyseas.' for 'pyseas.'

dark = {
        'font.weight' : 'medium',
        'font.color' : '#848b9b',
        'grid.alpha': 0.5,
        'grid.color': '#b0b0b0',
        'grid.linestyle': '-',
        'grid.linewidth': 0.4,
        'axes.prop_cycle' : _dark_track_cycler,
        'font.family' : 'Roboto', 
        'font.weight' : 'medium',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'ytick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'figure.titleweight' : 'medium',
         'axes.edgecolor' : '#848b9b',
         'text.color' : _colors.dark.title,
         'pyseas.fig.background' : _colors.dark.background,
         'pyseas.land.color' : _colors.dark.land,
         'pyseas.border.color' : _colors.dark.border,
         'pyseas.border.linewidth' : 0.4,
         'pyseas.ocean.color' : _colors.dark.ocean,
         'pyseas.eez.bordercolor' : _colors.dark.eez,
         'pyseas.eez.linewidth' : 0.4,
         'pyseas.map.centrallongitude' : 0,
         'pyseas.map.cmapsrc' : _cm.dark,
         'pyseas.map.trackprops' : _dark_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : 9,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo.name' : 'white_logo.png',
         'pyseas.logo.base_scale' : 0.025,
         'pyseas.logo.alpha' : 0.5,
         }

light = {
        'font.weight' : 'medium',
        'font.color' : '#848b9b',
         'grid.alpha': 0.5,
         'grid.color': '#b0b0b0',
         'grid.linestyle': '-',
         'grid.linewidth': 0.4,
         'axes.prop_cycle' : _light_track_cycler,
         'font.family' : 'Roboto', 
         'font.weight' : 'normal',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'ytick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'axes.edgecolor' : '#848b9b',
         'figure.titleweight' : 'medium',
         'text.color' : _colors.light.title,
         'pyseas.fig.background' : _colors.light.background,
         'pyseas.land.color' : _colors.light.land,
         'pyseas.border.color' : _colors.light.border,
         'pyseas.border.linewidth' : 0.4,
         'pyseas.ocean.color' : _colors.light.ocean,
         'pyseas.eez.bordercolor' : _colors.light.eez,
         'pyseas.eez.linewidth' : 0.4,
         'pyseas.map.centrallongitude' : 0,
         'pyseas.map.cmapsrc' : _cm.light,
         'pyseas.map.trackprops' : _light_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : 9,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo.name' : 'black_logo.png',
         'pyseas.logo.base_scale' : 0.025,
         'pyseas.logo.alpha' : 0.5,
         }


chart = {
         'grid.alpha': 0.5,
         'grid.color': '#b0b0b0',
         'grid.linestyle': '-',
         'grid.linewidth': 0.4,
         'axes.prop_cycle' : _chart_cycler,
         'font.family' : 'Roboto', 
         'font.weight' : 'normal',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'axes.edgecolor' : '#848b9b',
         'figure.titleweight' : 'medium',
         'text.color' : _colors.chart.title,
         'pyseas.fig.background' : _colors.chart.background,
         'pyseas.border.color' : _colors.chart.axes,
         'pyseas.border.linewidth' : 0.4,
         'pyseas.logo.name' : 'black_logo.png',
         'pyseas.logo.base_scale' : 0.025,
         'pyseas.logo.alpha' : 0.5,
         }


for k in dark:
    if k.startswith('pyseas.'):
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = dark[k]
del k

