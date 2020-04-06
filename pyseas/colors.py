from collections import namedtuple as _namedtuple
import os as _os
import json as _json

_MapPalette = _namedtuple('MapPalette', ['land', 'ocean', 'border',
    'background', 'highlight', 'title', 'eez', 'scale', 'colors'])

_ChartPalette = _namedtuple('ChartPalette', ['title', 'subtitle',
    'legend', 'axis_labels', 'axes', 'other_data', 'background', 'colors'])
_Tints = _namedtuple('Tints', ['p100', 'p80', 'p60', 'p40', 'p20'])


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



# chart = _ChartPalette(
#     title = '#363c4c',
#     subtitle = '#363c4c',

#     legend = '#848b9b',
#     axis_labels = '#848b9b',

#     axes = '#e6e7eb',
#     other_data = '#e6e7eb',

#     background = '#f7f7f7',

#     # List of lists with 
#     colors = (_Tints('#204280', '#4b5b91', '#7277a4', '#989abc', '#c5c6d9'), # 1
#               _Tints('#ee6256', '#f1816f', '#f59e8b', '#f8bdad', '#fcdcd1'), # 2
#               _Tints('#ad2176', '#b9558a', '#c77ca1', '#d6a2bb', '#e7cdda'), # 3
#               _Tints('#f8ba47', '#f9c66d', '#fbd38f', '#fde0b1', '#feeed5'), # 4
#               _Tints('#742980', '#875092', '#9d74a6', '#9d74a6', '#d6c7db'), # 5
#               _Tints('#f68d4b', '#f8a26b', '#fbb78a', '#fdceac', '#fee4d1'), # 6
#               _Tints('#d73b68', '#dd677e', '#e48b97', '#e48b97', '#d73568'), # 7
#               _Tints('#ebe55d', '#eee981', '#f2eda0', '#f5f3bf', '#f9f8dd')  # 8

#               ),
# )

