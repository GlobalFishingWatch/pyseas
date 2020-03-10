from matplotlib import pyplot as _plt
from matplotlib import rcsetup as _rcsetup
from . import colors as _colors

#TODO: check axes colors for light / dark

dark = {'font.family' : 'Roboto', 
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'figure.facecolor' : _colors.dark.background,
         'gfw.land.land' : _colors.dark.land,
         'gfw.border.color' : _colors.dark.border,
         'gfw.border.linewidth' : 0.4,
         'gfw.ocean.color' : _colors.dark.ocean,
         'gfw.eez.bordercolor' : _colors.dark.eez}

light = {'font.family' : 'Roboto', 
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'figure.facecolor' : _colors.dark.background,
         'gfw.land.land' : _colors.light.land,
         'gfw.border.color' : _colors.light.border,
         'gfw.border.linewidth' : 0.4,
         'gfw.ocean.color' : _colors.light.ocean,
         'gfw.eez.bordercolor' : _colors.light.eez}


for k in dark:
    if k.startswith('gfw.'):
        # TODO: add validation
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = dark[k]
del k

