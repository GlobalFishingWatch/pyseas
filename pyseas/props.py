from collections import namedtuple as _namedtuple
import os as _os
import json as _json

_MapPalette = _namedtuple('MapPalette', ['land', 'ocean', 'border',
    'background', 'highlight', 'title', 'eez', 'scale', 'track',
    'grid', 'tick', 'label', 'frame'])

_ChartPalette = _namedtuple('ChartPalette', ['title', 'subtitle',
    'legend', 'axis_labels', 'axes', 'other_data', 'background', 'colors'])
_Tints = _namedtuple('Tints', ['p100', 'p80', 'p60', 'p40', 'p20'])

_FishingPalette = _namedtuple('FishingPalette', ['fishing', 'non_fishing', 'undefined'])

class Props(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
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
            if (k1, k2) == ('chart', 'colors'):
                continue
            obj[k1][k2] = Props(**v2)
    for i, tints in enumerate(obj['chart']['colors']):
        obj['chart']['colors'][i] = _Tints(*tints)
    return obj

color_info = _load_colors()

dark = _MapPalette(**color_info['dark'])
light = _MapPalette(**color_info['light'])
chart = _ChartPalette(**color_info['chart'])
fishing = _FishingPalette(**color_info['fishing'])



