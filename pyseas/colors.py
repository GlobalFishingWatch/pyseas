from collections import namedtuple as _namedtuple
import os as _os
import json as _json

_MapPalette = _namedtuple('MapPalette', ['land', 'ocean', 'border',
    'background', 'highlight', 'title', 'eez', 'scale', 'colors',
    'grid', 'ticks', 'labels', 'frame'])

_ChartPalette = _namedtuple('ChartPalette', ['title', 'subtitle',
    'legend', 'axis_labels', 'axes', 'other_data', 'background', 'colors'])
_Tints = _namedtuple('Tints', ['p100', 'p80', 'p60', 'p40', 'p20'])

_FishingPalette = _namedtuple('FishingPalette', ['fishing', 'non_fishing', 'undefined'])

_root = _os.path.dirname(_os.path.dirname(__file__))

def _load_colors():
    path = _os.path.join(_root, 'data/color_info.json')
    with open(path) as f:
        obj = _json.load(f)
    for i, tints in enumerate(obj['chart']['colors']):
        obj['chart']['colors'][i] = _Tints(*tints)
    return obj

color_info = _load_colors()

dark = _MapPalette(**color_info['dark'])
light = _MapPalette(**color_info['light'])
chart = _ChartPalette(**color_info['chart'])
fishing = _FishingPalette(**color_info['fishing'])



