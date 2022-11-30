# Based on this stackoverflow post:
# https://stackoverflow.com/questions/27962953/cartopy-axis-label-workaround
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sgeom
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER


def find_side(ls, side):
    """
    Given a shapely LineString which is assumed to be rectangular, return the
    line corresponding to a given side of the rectangle.

    """
    minx, miny, maxx, maxy = ls.bounds
    points = {
        "left": [(minx, miny), (minx, maxy)],
        "right": [(maxx, miny), (maxx, maxy)],
        "bottom": [(minx, miny), (maxx, miny)],
        "top": [(minx, maxy), (maxx, maxy)],
    }
    return sgeom.LineString(points[side])


# Pad the lines we use to compute intersections with the outside of the
# map so we don't miss intersections
EPS = 1  # degrees


def draw_xticks(ax, ticks, side="bottom"):
    """Draw ticks on the bottom x-axis of a cartopy map."""
    assert side in ["bottom", "top"]
    te = lambda xy: xy[0]
    lc = lambda t, n, b: np.vstack(
        (np.zeros(n) + t, np.linspace(b[2] - EPS, b[3] + EPS, n))
    ).T
    xticks, xticklabels = _ticks(ax, ticks, side, lc, te)
    if side == "bottom":
        ax.xaxis.tick_bottom()
    else:
        ax.xaxis.tick_top()
    ax.set_xticks(xticks)
    ax.set_xticklabels([ax.xaxis.get_major_formatter()(xtick) for xtick in xticklabels])


def draw_yticks(ax, ticks, side="left"):
    """Draw ticks on the left y-axis of a Lamber Conformal projection."""
    assert side in ["left", "right"]
    te = lambda xy: xy[1]
    lc = lambda t, n, b: np.vstack(
        (np.linspace(b[0] - EPS, b[1] + EPS, n), np.zeros(n) + t)
    ).T
    yticks, yticklabels = _ticks(ax, ticks, side, lc, te)
    if side == "left":
        ax.yaxis.tick_left()
    else:
        ax.yaxis.tick_right()
    ax.set_yticks(yticks)
    ax.set_yticklabels([ax.yaxis.get_major_formatter()(ytick) for ytick in yticklabels])


def _ticks(ax, ticks, tick_location, line_constructor, tick_extractor):
    """Get the tick locations and labels for an axis of a Lambert Conformal projection."""
    try:
        patch = ax.outline_patch
    except AttributeError:
        patch = ax.patch
    outline_patch = sgeom.LineString(patch.get_path().vertices.tolist())
    axis = find_side(outline_patch, tick_location)
    n_steps = 30
    extent = ax.get_extent(ccrs.PlateCarree())
    _ticks = []
    for t in ticks:
        xy = line_constructor(t, n_steps, extent)
        proj_xyz = ax.projection.transform_points(ccrs.Geodetic(), xy[:, 0], xy[:, 1])
        xyt = proj_xyz[..., :2]
        ls = sgeom.LineString(xyt.tolist())
        locs = axis.intersection(ls)
        if not locs:
            tick = [None]
        else:
            if isinstance(locs, sgeom.MultiPoint):
                locs = locs.geoms[0]
            tick = tick_extractor(locs.xy)
        _ticks.append(tick[0])
    # Remove ticks that aren't visible:
    ticklabels = list(ticks)
    while True:
        try:
            index = _ticks.index(None)
        except ValueError:
            break
        _ticks.pop(index)
        ticklabels.pop(index)
    return _ticks, ticklabels
