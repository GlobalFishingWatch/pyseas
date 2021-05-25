from matplotlib.style import context, use
__version__ = "0.2.0"


def _reload():
    """Reload modules during development

    Note: Not 100% reliable!
    """
    import pyseas
    from pyseas import maps, cm, styles, util, props
    from pyseas.contrib import plot_tracks
    from pyseas.maps import (scalebar, core, rasters, ticks, projection, overlays,
                             rasterize)
    from pyseas import contrib
    import imp

    imp.reload(pyseas)
    imp.reload(util)
    imp.reload(ticks)
    imp.reload(scalebar)
    imp.reload(props)
    imp.reload(cm)
    imp.reload(styles)
    imp.reload(rasters)
    imp.reload(rasterize)
    imp.reload(core)
    imp.reload(maps)
    imp.reload(plot_tracks)
    imp.reload(pyseas)
    imp.reload(projection)
    imp.reload(overlays)
    contrib._reload()



