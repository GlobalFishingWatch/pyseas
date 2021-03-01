from collections import namedtuple as _namedtuple
import os as _os
import json as _json

class Props(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k[0] in '0123456789':
                k = '_' + k
            if isinstance(v, dict):
                v = Props(**v)
            setattr(self, k, v)

    def __repr__(self):
        if len(self.__dict__) <= 3:
            lines = ', '.join("{}={!r}".format(k, v) for (k, v) in self.__dict__.items())
            return "Props({})".format(lines)
        else:
            lines = ',\n'.join("  {} = {!r}".format(k, v) for (k, v) in self.__dict__.items())
            return "Props(\n  {}\n)".format(lines)

    __str__ = __repr__

_root = _os.path.dirname(__file__)

def _load_props():
    path = _os.path.join(_root, 'data/props.json')
    with open(path) as f:
        obj = _json.load(f)
    for k1, v1 in obj.items():
        for k2, v2 in v1.items():
            obj[k1][k2] = Props(**v2)
    return obj

raw_props = _load_props()

dark = Props(**raw_props['dark'])
light = Props(**raw_props['light'])
fishing = Props(**raw_props['fishing'])
chart = Props(**raw_props['chart'])


