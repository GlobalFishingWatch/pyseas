from collections import namedtuple
import numpy as np
import cartopy.crs
from ..util import asarray, lon_avg


DEFAULT_PADDING_DEG = 0.1
MAX_LAMBERT_EXTENT = 90

ProjectionInfo = namedtuple(
    "ProjectionInfo",
    ["projection", "extent", "description", "central_longitude", "central_latitude"],
)


def find_projection(lons, lats, pad_rel=0.2, pad_abs=0.1, percentile=99.9):
    """Find a suitable projection and extent for a set of lat lon points.

    Projection will include most points, but only forces `percentile` of them
    to be within the projection to allow for outliers.

    Parameters
    ----------
    lons : array of float
    lats : array of float
    pad_rel : float, optional
        Base extent is padded by this times base extent size.
    pad_abs : float, optional
        Base extent is padded by this many degrees.
    percentile : float, optional
        Fraction of points to force into projection extents.

    Returns
    -------
    ProjectionInfo
        A namedtuple containing `projection`, `extent`, `description`, `central_longitude`,
        and `central_latitude`.

    """
    lons, lats = (asarray(x) for x in (lons, lats))
    assert len(lons) == len(lats), (len(lons), len(lats))
    lonm0 = lon_avg(lons)
    lons = (lons - lonm0 + 180) % 360 + lonm0 - 180
    lon0, lonm, lon1 = np.percentile(lons, (100 - percentile, 50, percentile))
    (lon0, lon1) = [(x - lonm + 180) % 360 + lonm - 180 for x in (lon0, lon1)]
    if lon0 > lon1:
        lon0, lon1 = lon1, lon0
    lat0, latm, lat1 = np.percentile(lats, (100 - percentile, 50, percentile))
    lon_delta = abs(lon1 - lon0) * pad_rel + pad_abs
    lat_delta = abs(lat1 - lat0) * pad_rel + pad_abs

    extent = (lon0 - lon_delta, lon1 + lon_delta, lat0 - lat_delta, lat1 + lat_delta)
    if (
        extent[1] - extent[0] <= MAX_LAMBERT_EXTENT
        and extent[3] - extent[2] <= MAX_LAMBERT_EXTENT
    ):
        projection = cartopy.crs.LambertAzimuthalEqualArea(
            central_longitude=lonm, central_latitude=latm
        )
        lonstr = ("{}°E" if (lonm >= 0) else "{}°W").format(int(round(abs(lonm))))
        latstr = ("{}°N" if (latm >= 0) else "{}°S").format(int(round(abs(latm))))
        description = "Lambert azimuthal equal area @{},{}".format(lonstr, latstr)
    else:
        extent = None
        latm = None
        projection = cartopy.crs.EqualEarth(central_longitude=lonm)
        lonstr = ("{}°E" if (lonm >= 0) else "{}°W").format(int(round(abs(lonm))))
        description = "EqualEarth @{}".format(
            lonstr,
        )
    return ProjectionInfo(
        projection, extent, description, central_longitude=lonm, central_latitude=latm
    )
