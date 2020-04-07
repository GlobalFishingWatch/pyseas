from matplotlib import pyplot as _plt
from matplotlib import rcsetup as _rcsetup
from . import props as _props
from . import cm as _cm
from cycler import cycler
from matplotlib.colors import to_rgba


_light_track_cycler = cycler(color=_props.light.track.colors)
_light_artist_cycler = cycler(edgecolor=_props.light.track.colors, 
        facecolor=[(0, 0, 0, 0)]*len(_props.light.track.colors))
_dark_track_cycler = cycler(color=_props.dark.track.colors)
_dark_artist_cycler = cycler(edgecolor=_props.dark.track.colors, 
    facecolor=[(0, 0, 0, 0)]*len(_props.dark.track.colors))

_chart_colors = []
for clr in _props.chart.colors._100_percent:
    _chart_colors.append(clr)

_chart_cycler = cycler(color=_chart_colors, linewidth=[2]*len(_chart_colors))
del cycler, _chart_colors, clr


_undef = dict(edgecolor=_props.fishing.undefined.color, facecolor='none', 
                        linewidth=_props.fishing.undefined.width,
                        alpha=_props.fishing.undefined.alpha)
_nonfishprops = dict(edgecolor=_props.fishing.non_fishing.color, facecolor='none', 
                        linewidth=_props.fishing.non_fishing.width,
                        alpha=_props.fishing.non_fishing.alpha)
_fishprops = dict(edgecolor=_props.fishing.fishing.color, facecolor='none', 
                        linewidth=_props.fishing.fishing.width,
                        alpha=_props.fishing.fishing.alpha) 
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
         'pyseas.eez.bordercolor' : _props.dark.eez.color,
         'pyseas.eez.linewidth' : _props.dark.eez.width,
         'pyseas.map.cmapsrc' : _cm.dark,
         'pyseas.map.trackprops' : _dark_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : _props.dark.projection_label.size,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo.name' : _props.dark.logo.name,
         'pyseas.logo.base_scale' : _props.dark.logo.base_scale,
         'pyseas.logo.alpha' : _props.dark.logo.alpha,
         }

light = {
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
         'pyseas.eez.bordercolor' : _props.light.eez.color,
         'pyseas.eez.linewidth' : _props.light.eez.width,
         'pyseas.map.cmapsrc' : _cm.light,
         'pyseas.map.trackprops' : _light_artist_cycler,
         'pyseas.map.fishingprops' : _fishing_props,
         'pyseas.map.annotationmapprops' : _annotationmapprops,
         'pyseas.map.annotationplotprops' : _annotationplotprops,
         'pyseas.map.projlabelsize' : _props.dark.projection_label.size,
         'pyseas.map.colorbarlabelfont' : _colorbarlabelfont,
         'pyseas.logo.name' : _props.light.logo.name,
         'pyseas.logo.base_scale' : _props.light.logo.base_scale,
         'pyseas.logo.alpha' : _props.light.logo.alpha,
         }


chart = {
         'grid.alpha': 0.5,
         'grid.color': '#b0b0b0',
         'grid.linestyle': '-',
         'grid.linewidth': 0.4,
         'axes.prop_cycle' : _chart_cycler,
         'font.family' : 'Roboto', 
         'font.weight' : 'medium',
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'axes.labelweight' : 'medium',
         'axes.titleweight' : 'medium',
         'axes.edgecolor' : '#848b9b',
         'figure.titleweight' : 'medium',
         'text.color' : _props.chart.title.color,
         'pyseas.fig.background' : _props.chart.background.color,
         'pyseas.border.color' : _props.chart.axes.color,
         'pyseas.border.linewidth' : 0.4,
         'pyseas.logo.name' : _props.light.logo.name,
         'pyseas.logo.base_scale' : _props.light.logo.base_scale,
         'pyseas.logo.alpha' : _props.light.logo.alpha,
         }


for k in dark:
    if k.startswith('pyseas.'):
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = dark[k]
del k

