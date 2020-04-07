from collections import namedtuple as _namedtuple
import os as _os
import json as _json

_MapPalette = _namedtuple('MapPalette', ['land', 'ocean', 'border',
    'background', 'highlight', 'title', 'eez', 'scale', 'track',
    'grid', 'tick', 'label', 'frame', 'logo'])

_ChartPalette = _namedtuple('ChartPalette', ['title', 'subtitle',
    'legend', 'axis_labels', 'axes', 'other_data', 'background', 'colors'])

_FishingPalette = _namedtuple('FishingPalette', ['fishing', 'non_fishing', 'undefined'])

class Props(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k[0] in '0123456789':
                k = '_' + k
            setattr(self, k, v)

    def __repr__(self):
        if len(self.__dict__) <= 3:
            lines = ', '.join("{}={!r}".format(k, v) for (k, v) in self.__dict__.items())
            return "Props({})".format(lines)
        else:
            lines = ',\n'.join("  {} = {!r}".format(k, v) for (k, v) in self.__dict__.items())
            return "Props(\n  {}\n)".format(lines)

    __str__ = __repr__

_root = _os.path.dirname(_os.path.dirname(__file__))

def _load_colors():
    path = _os.path.join(_root, 'data/props.json')
    with open(path) as f:
        obj = _json.load(f)
    for k1, v1 in obj.items():
        for k2, v2 in v1.items():
            obj[k1][k2] = Props(**v2)
    return obj

color_info = _load_colors()

dark = _MapPalette(**color_info['dark'])
light = _MapPalette(**color_info['light'])
chart = _ChartPalette(**color_info['chart'])
fishing = _FishingPalette(**color_info['fishing'])



