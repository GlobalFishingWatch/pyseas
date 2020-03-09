"""GFW Colormaps

Official GFW Colormaps
----------------------
reception
fishing
presence


Unofficial GFW Colormaps
------------------------

Colormaps made by Juan Carlos:

unofficial.jc_presence
unofficial.jc_reception
unofficial.jc_linearorange
unofficial.jc_linearblue
unofficial.jc_linearpink
"""
from matplotlib import colors
import numpy as np


def _hex2cmap(name, hex_colors):
    '''Convert sequence of hex colors to matplotlib cmap

    Parameters
    ----------
    name : str
    hex_colors : sequence of str
        Must be in '#RRGGBB' format

    Returns
    -------
    LinearSegmentedColormap
    '''
    def ramp(i0, i1):
        float_colors = [(int(x[i0:i1], 16) / 256.0) for x in hex_colors]
        ramp = zip(np.linspace(0, 1, len(hex_colors), endpoint=True), float_colors, float_colors)
        return tuple(ramp)

    cdict = { 'red': ramp(1, 3),
              'green': ramp(3, 5),
              'blue':  ramp(5, 7) }

    cmap = colors.LinearSegmentedColormap(name, cdict, 256)
    cmap.set_bad(alpha = 0.0)
    return cmap


reception = _hex2cmap('reception', ('#ff4573', '#7b2e8d', '#093b76', '#0c276c')) 
fishing = _hex2cmap('fishing', ('#0c276c', '#3b9088', '#eeff00', '#ffffff')) 
presence = _hex2cmap('presence', ('#0c276c', '#114685','#00ffc3','#ffffff'))

class _Unofficial(object):
  jc_presence  = _hex2cmap('jc_presence', ('#3359A8', '#16A3A4', '#00FFC3', '#ffffff'))
  jc_reception = _hex2cmap('jc_reception', ('#5E0C20', '#2927A8', '#41FFA7', '#ffffff'))
  jc_linearorange = _hex2cmap('jc_linearorange', ('#0C276C', '#824158', '#FF9500', '#ffffff'))
  jc_linearblue = _hex2cmap('jc_linearblue', ('#0C276C', '#1D5780', '#00FFC3', '#ffffff'))
  jc_linearpink = _hex2cmap('jc_linearpink', ('#0C276C', '#4E289B', '#F74559', '#ffffff'))

unofficial = _Unofficial()
