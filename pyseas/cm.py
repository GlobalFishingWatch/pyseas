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


BivariateColormaps
------------------

## Factory functions to create bivariate colormaps
bivariate.TransparencyBivariateColormap
bivariate.SummedBivariateColormap

## Colormaps suitable for use with TransparencyBivariateColormap
bivariate.orange_blue
bivariate.blue_orange


"""
from matplotlib import colors as _colors
import numpy as _np
import skimage.color as _skcolor


def _hex2cmap(name, hex_colors, flip=False):
    """Convert sequence of hex colors to matplotlib cmap

    Parameters
    ----------
    name : str
    hex_colors : sequence of str
        Must be in '#RRGGBB' format

    Returns
    -------
    LinearSegmentedColormap
    """
    if flip:
        hex_colors = hex_colors[::-1]

    def ramp(i0, i1):
        float_colors = [(int(x[i0:i1], 16) / 256.0) for x in hex_colors]
        ramp = zip(
            _np.linspace(0, 1, len(hex_colors), endpoint=True),
            float_colors,
            float_colors,
        )
        return tuple(ramp)

    cdict = {"red": ramp(1, 3), "green": ramp(3, 5), "blue": ramp(5, 7)}

    cmap = _colors.LinearSegmentedColormap(name, cdict, 256)
    cmap.set_bad(alpha=0.0)
    return cmap


class _Dark:
    reception = _hex2cmap("reception", ("#ff4573", "#7b2e8d", "#093b76", "#0c276c"))
    fishing = _hex2cmap("fishing", ("#0c276c", "#3b9088", "#eeff00", "#ffffff"))
    presence = _hex2cmap("presence", ("#0c276c", "#114685", "#00ffc3", "#ffffff"))


dark = _Dark()


class _Light:
    reception = _hex2cmap(
        "reception", ("#ff4573", "#7b2e8d", "#093b76", "#0c276c"), flip=True
    )
    fishing = _hex2cmap(
        "fishing", ("#0c276c", "#3b9088", "#eeff00", "#ffffff"), flip=True
    )
    presence = _hex2cmap(
        "presence", ("#0c276c", "#114685", "#00ffc3", "#ffffff"), flip=True
    )


light = _Light()


class _Bivariate:
    blue_orange = _colors.LinearSegmentedColormap.from_list(
        "blue_orange",
        [
            "#FF7E00",
            "#F18352",
            "#E08979",
            "#CC8F99",
            "#B496B4",
            "#999CCC",
            "#79A1E0",
            "#52A6F1",
            "#00AAFF",
        ][::-1],
    )
    orange_blue = blue_orange.reversed
    bright_blue_orange = _colors.LinearSegmentedColormap.from_list(
        "bright_blue_orange",
        [
            "#0062F0",
            "#405FF2",
            "#645BE1",
            "#855ECF",
            "#A463BB",
            "#BB63A3",
            "#D06286",
            "#E16063",
            "#F2613B",
            "#F56A00",
        ],
    )
    bright_blue_orange = bright_blue_orange.reversed
    aqua = _colors.LinearSegmentedColormap.from_list(
        "aqua", [(0.95, 0.95, 0.95), (0.39, 0.53, 1.0)]
    )
    orange = _colors.LinearSegmentedColormap.from_list(
        "orange", [(0.95, 0.95, 0.95), (1.0, 0.25, 0.0)]
    )
    lime = _colors.LinearSegmentedColormap.from_list(
        "lime", [(0.95, 0.95, 0.95), (0.39, 1.0, 0.53)]
    )
    pink = _colors.LinearSegmentedColormap.from_list(
        "pink", [(0.95, 0.95, 0.95), (1.0, 0.48, 0.66)]
    )
    from .maps.bivariate import TransparencyBivariateColormap
    from .maps.bivariate import MinBivariateColormap
    from .maps.bivariate import MaxBivariateColormap


bivariate = _Bivariate()


class _Misc:
    blue_orange = bivariate.blue_orange
    orange_blue = bivariate.orange_blue
    jc_presence = _hex2cmap("jc_presence", ("#3359A8", "#16A3A4", "#00FFC3", "#ffffff"))
    jc_reception = _hex2cmap(
        "jc_reception", ("#5E0C20", "#2927A8", "#41FFA7", "#ffffff")
    )
    jc_linearorange = _hex2cmap(
        "jc_linearorange", ("#0C276C", "#824158", "#FF9500", "#ffffff")
    )
    jc_linearblue = _hex2cmap(
        "jc_linearblue", ("#0C276C", "#1D5780", "#00FFC3", "#ffffff")
    )
    jc_linearpink = _hex2cmap(
        "jc_linearpink", ("#0C276C", "#4E289B", "#F74559", "#ffffff")
    )


misc = unofficial = _Misc()
