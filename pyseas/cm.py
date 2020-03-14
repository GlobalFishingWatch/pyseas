"""GFW Colormaps

Official GFW Colormaps
----------------------

Colormaps for dark style:

dark.reception
dark.fishing
dark.presence

Colormaps for light style:

light.reception
light.fishing
light.presence


Unofficial GFW Colormaps
------------------------

Colormaps made by Juan Carlos:

unofficial.jc_presence
unofficial.jc_reception
unofficial.jc_linearorange
unofficial.jc_linearblue
unofficial.jc_linearpink
"""
from matplotlib import colors as _colors
import numpy as _np
import skimage.color as _skcolor


def _flip_colors(hexcodes):
    # import numpy as np
    # def hex2rgb(code):
    #     return [int(x, 16) / 255.0 for x in [code[1:3], code[3:5], code[5:7]]]
    # def rgb2hex(vals):
    #     return '#' + ''.join('{:02X}'.format(int(round(255 * x))) for x in vals)
    # rgb = np.array([hex2rgb(x) for x in hexcodes])[None, :, :]
    # hsv = _skcolor.rgb2hsv(rgb)
    # hsv[:, :, 1] = np.array(hsv[:, ::-1, 1])
    # hsv[:, :, 2] = np.array(hsv[:, ::-1, 2])
    # rgb = _skcolor.hsv2rgb(hsv)
    # hexcodes = [rgb2hex(x) for x in rgb[0]]
    return hexcodes[::-1]


def _hex2cmap(name, hex_colors, flip=False):
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
    if flip:
        hex_colors = _flip_colors(hex_colors)
    def ramp(i0, i1):
        float_colors = [(int(x[i0:i1], 16) / 256.0) for x in hex_colors]
        ramp = zip(_np.linspace(0, 1, len(hex_colors), endpoint=True), float_colors, float_colors)
        return tuple(ramp)

    cdict = { 'red': ramp(1, 3),
              'green': ramp(3, 5),
              'blue':  ramp(5, 7) }

    cmap = _colors.LinearSegmentedColormap(name, cdict, 256)
    cmap.set_bad(alpha = 0.0)
    return cmap

class _Dark(object):
    reception = _hex2cmap('reception', ('#ff4573', '#7b2e8d', '#093b76', '#0c276c')) 
    fishing = _hex2cmap('fishing', ('#0c276c', '#3b9088', '#eeff00', '#ffffff')) 
    presence = _hex2cmap('presence', ('#0c276c', '#114685','#00ffc3','#ffffff'))
dark = _Dark()

class _Light(object):
    reception = _hex2cmap('reception', ('#ff4573', '#7b2e8d', '#093b76', '#0c276c'), 
        flip=True) 
    fishing = _hex2cmap('fishing', ('#0c276c', '#3b9088', '#eeff00', '#ffffff'),
        flip=True) 
    presence = _hex2cmap('presence', ('#0c276c', '#114685','#00ffc3','#ffffff'),
        flip=True)
light = _Light()


class _Unofficial(object):
  jc_presence  = _hex2cmap('jc_presence', ('#3359A8', '#16A3A4', '#00FFC3', '#ffffff'))
  jc_reception = _hex2cmap('jc_reception', ('#5E0C20', '#2927A8', '#41FFA7', '#ffffff'))
  jc_linearorange = _hex2cmap('jc_linearorange', ('#0C276C', '#824158', '#FF9500', '#ffffff'))
  jc_linearblue = _hex2cmap('jc_linearblue', ('#0C276C', '#1D5780', '#00FFC3', '#ffffff'))
  jc_linearpink = _hex2cmap('jc_linearpink', ('#0C276C', '#4E289B', '#F74559', '#ffffff'))

unofficial = _Unofficial()
