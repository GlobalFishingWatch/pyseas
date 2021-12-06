from collections import namedtuple
import json
import math
import numpy as np
import os
import cartopy.crs
from ..util import asarray, lon_avg


identity = cartopy.crs.PlateCarree()

root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

_projections = {
    "EqualEarth": cartopy.crs.EqualEarth,
    "LambertAzimuthalEqualArea": cartopy.crs.LambertAzimuthalEqualArea,
    "AlbersEqualArea": cartopy.crs.AlbersEqualArea,
    "LambertCylindrical": cartopy.crs.LambertCylindrical,
}


def load_projections():

    path = os.path.join(root, "pyseas/data/projection_info.json")
    with open(path) as f:
        info = json.load(f)
    for k, v in info.items():
        v["projection"] = _projections[v["projection"]]
        info[k] = v
    return info


projection_info = load_projections()


def get_projection(projinfo):
    if isinstance(projinfo, ProjectionInfo):
        return projinfo.projection
    info = projection_info[projinfo]
    return info["projection"](**info["args"])


def get_extent(projinfo):
    if isinstance(projinfo, ProjectionInfo):
        return projinfo.extent
    return projection_info[projinfo]["extent"]


def get_proj_description(projinfo):
    if isinstance(projinfo, ProjectionInfo):
        return projinfo.description
    return projection_info[projinfo]["description"]


DEFAULT_PADDING_DEG = 0.1
MAX_LAMBERT_EXTENT = 90

ProjectionInfo = namedtuple(
    "ProjectionInfo",
    ["projection", "extent", "description", "central_longitude", "central_latitude"],
)


def find_projection_core(lons, lats, pad_rel=0.2, pad_abs=0.1, percentile=99.9):
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
        and `central_latitude`. Projection here is the projection *name*

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
        projection = "LambertAzimuthalEqualArea"
        lonstr = ("{}°E" if (lonm >= 0) else "{}°W").format(int(round(abs(lonm))))
        latstr = ("{}°N" if (latm >= 0) else "{}°S").format(int(round(abs(latm))))
        description = "Lambert azimuthal equal area @{},{}".format(lonstr, latstr)
    else:
        extent = None
        latm = None
        projection = "EqualEarth"
        lonstr = ("{}°E" if (lonm >= 0) else "{}°W").format(int(round(abs(lonm))))
        description = "EqualEarth @{}".format(
            lonstr,
        )
    return ProjectionInfo(
        projection, extent, description, central_longitude=lonm, central_latitude=latm
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
    info = find_projection_core(lons, lats, pad_rel, pad_abs, percentile)
    if info.projection == "LambertAzimuthalEqualArea":
        projection = cartopy.crs.LambertAzimuthalEqualArea(
            central_longitude=info.central_longitude,
            central_latitude=info.central_latitude,
        )
    elif info.projection == "EqualEarth":
        projection = cartopy.crs.EqualEarth(central_longitude=info.central_longitude)
    else:
        raise RuntimeError("unknown projection name")
    return info._replace(projection=projection)
