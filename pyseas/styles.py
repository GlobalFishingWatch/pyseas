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
         'gfw.colors.land' : _colors.dark.land,
         'gfw.colors.border' : _colors.dark.border,
         'gfw.border.linewidth' : 0.4,
         'gfw.colors.ocean' : _colors.dark.ocean}

light = {'font.family' : 'Roboto', 
         'xtick.color' : '#848b9b',
         'ytick.color' : '#848b9b',
         'xtick.labelsize' : 11,
         'axes.labelsize' : 11,
         'axes.labelcolor' : '#848b9b',
         'gfw.colors.land' : _colors.light.land,
         'gfw.colors.border' : _colors.light.border,
         'gfw.border.edgewidth' : 0.4,
         'gfw.colors.ocean' : _colors.light.ocean}


for k in dark:
    if k.startswith('gfw.'):
        # TODO: add validation
        _plt.rcParams.validate[k] = _rcsetup.validate_any # No validation for now
        _plt.rcParams[k] = dark[k]
del k

