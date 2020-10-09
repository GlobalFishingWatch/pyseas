from matplotlib.pyplot import rc_context as context
__version__ = "0.0.5"


def _reload():
    """Reload modules during development

    Note: Not 100% reliable!
    """
    import pyseas
    from pyseas import maps, cm, styles, util, props
    from pyseas.contrib import plot_tracks
    from pyseas.maps import scalebar, core, rasters, ticks, projection
    import imp

    imp.reload(util)
    imp.reload(ticks)
    imp.reload(scalebar)
    imp.reload(props)
    imp.reload(cm)
    imp.reload(styles)
    imp.reload(rasters)
    imp.reload(core)
    imp.reload(maps)
    imp.reload(plot_tracks)
    imp.reload(pyseas)
    imp.reload(projection)


