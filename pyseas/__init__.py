import os
import subprocess

from matplotlib.style import context, use  # NOQA

__version__ = "0.8.1"


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
    import imp

    imp.reload(pyseas)
    imp.reload(util)
    imp.reload(projection)
    imp.reload(ticks)
    imp.reload(scalebar)
    imp.reload(props)
    imp.reload(cm)
    imp.reload(styles)
    imp.reload(rasters)
    imp.reload(rasterize)
    imp.reload(colorbar)
    imp.reload(bivariate)
    imp.reload(core)
    imp.reload(maps)
    imp.reload(extent)

    imp.reload(plot_tracks)
    imp.reload(pyseas)
    imp.reload(overlays)
    contrib._reload()
