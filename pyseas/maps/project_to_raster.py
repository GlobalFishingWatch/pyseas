import numpy as np

from . import core
from . import h3_dgg 

# TODO: rename to project_to_raster.py



def project_h3(ax, h3cnts): 
    """TODO: fill in
    """
    xvals, yvals, tx = setup_composite_tx(ax)
    return h3_dgg.h3cnts_to_raster(h3cnts, xvals, yvals, tx)  # rename to project_h3cnts  


def project_raster(ax, raster, extent, origin='upper'):
    """Convert raster in lat/lon coordinates into one in projection coordinates
    
    Parameters
    ----------
    ax: matplotlib Axes
    raster : 2D array of float

    Returns
    -------
    2D array of float
    """
    xvals, yvals, tx = setup_composite_tx(ax)
    return raster_to_raster(raster, extent, xvals, yvals, tx, origin=origin)  


def setup_composite_tx(ax):
    (i0, j0), (i1, j1) = ax.transAxes.transform([(0, 0), (1, 1)])
    xvals = np.arange(i0, i1)
    yvals = np.arange(j0, j1)
    def composite_tx(ijs):
        yxs = np.asarray(ax.transData.inverted().transform(ijs))
        return core.identity.transform_points(ax.projection, yxs[:, 0], yxs[:, 1])[:, :2]
    return xvals, yvals, composite_tx


def raster_to_raster(raster, extent, xvals, yvals, transform, origin='upper'):
    assert origin in ('upper', 'lower')
    projected = np.zeros([len(yvals), len(xvals)])
    lon0, lon1, lat0, lat1 = extent
    if origin == 'upper':
        lat0, lat1 = lat1, lat0
    # TODO: Support second value > first, assuming rightward, but wrapped
    dlat = (lat1 - lat0) / raster.shape[0]
    dlon = (lon1 - lon0) / raster.shape[1]
    for i, y in enumerate(yvals):
        lons, lats = np.transpose(transform([(x, y) for x in xvals]))
        rr = ((lats - lat0) // dlat).astype(int)
        cc = ((lons - lon0) // dlon).astype(int)
        for j, (r, c) in enumerate(zip(rr, cc)):
            if 0 <= r < raster.shape[0] and 0 <= c < raster.shape[1]:
                projected[i, j] = raster[r, c]
    return projected