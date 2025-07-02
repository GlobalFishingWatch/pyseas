import os
import subprocess

from matplotlib.style import context, use  # NOQA

__version__ = "0.8.2"


base = os.path.dirname(__file__)
path = os.path.join(base, "doc", "Examples.ipynb")

__doc__ = f"""Library for plotting GFW style maps

To see some examples, run:

    jupyter notebook {path}
"""


del os, subprocess, base, path


def _reload():
    """Reload modules during development

    Note: Not 100% reliable!
    """
    import pyseas
    from pyseas import maps, cm, styles, util, props
    from pyseas.contrib import plot_tracks
    from pyseas.maps import (
        scalebar,
        core,
        extent,
        rasters,
        ticks,
        projection,
        overlays,
        rasterize,
        colorbar,
        bivariate,
    )
    from pyseas import contrib
    from importlib import reload
    \
    reload(pyseas)
    reload(util)
    reload(projection)
    reload(ticks)
    reload(scalebar)
    reload(props)
    reload(cm)
    reload(styles)
    reload(rasters)
    reload(rasterize)
    reload(colorbar)
    reload(bivariate)
    reload(core)
    reload(maps)
    reload(extent)

    reload(plot_tracks)
    reload(pyseas)
    reload(overlays)
    contrib._reload()
