import matplotlib.pyplot as plt

from .core import identity


def set_lon_extent(min_lon, max_lon, central_lat, ax=None):
    """Set plots longitudinal extents centered on given latitude

    Args:
        min_lon (float) : left edge of desired map
        max_lon (float) : right edge of desired map
        central_lat (float) : vertical center of desired map
        ax (GeoAxes, optional) : axes to set extent of
    """
    if ax is None:
        ax = plt.gca()
    ax.set_extent([min_lon, max_lon, central_lat, central_lat], crs=identity)
    ax.set_adjustable("datalim")


def set_lat_extent(min_lat, max_lat, central_lon, ax=None):
    """Set plots longitudinal extents centered on given latitude

    Args:
        min_lat (float) : bottom edge of desired map
        max_lat (float) : top edge of desired map
        central_lon (float) : horizonatl center of desired map
        ax (GeoAxes, optional) : axes to set extent of
    """
    if ax is None:
        ax = plt.gca()
    ax.set_extent([min_lat, max_lat, central_lon, central_lon], crs=identity)
    ax.set_adjustable("datalim")
