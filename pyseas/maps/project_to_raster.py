import numpy as np

from . import core
from . import h3_dgg 



def project_h3(ax, h3_data): 
    """Convert H3 data into one into a raster in projection coordinates
    
    Parameters
    ----------
    ax: matplotlib Axes
    h3_data : dict 
        Maps h3ids to int or float values

    Returns
    -------
    2D array of float
    """
    rr, cc, tx = setup_composite_tx(ax)
    return h3_dgg.h3cnts_to_raster(h3_data, rr, cc, tx) 


def project_raster(ax, raster, extent, origin='upper'):
    """Convert raster in lat/lon coordinates into one in projection coordinates
    
    Parameters
    ----------
    ax: matplotlib Axes
    raster : 2D array of float
    extent : tuple of float
        Borders of raster as (lon0, lon1, lat0, lat1) 
    origin : 'upper' or 'lower', optional
        Where the 0 point of the y-axis is located

    Returns
    -------
    2D array of float
    """
    rr, cc, tx = setup_composite_tx(ax)
    return raster_to_raster(raster, extent, rr, cc, tx, origin=origin)  


def setup_composite_tx(ax):
    """Return the transform and it's range in x and y

    Parameters
    ----------
    ax : matplotlib Axes

    Returns
    -------
    numpy array or row locations in output raster
    numpy array of column locations in output raster
    function of (rows, columns) -> (lons, lats)
    """
    (i0, j0), (i1, j1) = ax.transAxes.transform([(0, 0), (1, 1)])
    col_locs = np.arange(i0, i1)
    row_locs = np.arange(j0, j1)
    def composite_tx(rr, cc):
        # rr, cc -> lons, lats
        cr = list(zip(cc, rr))
        data_crds = np.asarray(ax.transData.inverted().transform(cr))
        lonlat = core.identity.transform_points(ax.projection, 
                                        data_crds[:, 0], data_crds[:, 1])[:, :2]
        return np.transpose(lonlat)
    return row_locs, col_locs, composite_tx


def raster_to_raster(raster, extent, row_locs, col_locs, transform, origin='upper'):
    """Convert raster defined in lat,lon space to raster in projected coords
    
    Parameters
    ----------
    raster : 2D array of float
    extent : tuple of float
        Borders of the raster as (lon0, lon1, lat0, lat1)
    row_locs : array of float
    col_locs : array of float
    transform : function of (rows, columns) -> (lons, lats)
    origin : 'upper' or 'lower', optional
        Where the 0 point of the y-axis is located

    Returns
    -------
    2D array of float
    """
    assert origin in ('upper', 'lower')
    projected = np.zeros([len(row_locs), len(col_locs)])
    lon0, lon1, lat0, lat1 = extent
    if origin == 'upper':
        lat0, lat1 = lat1, lat0
    # TODO: Support second value > first, assuming rightward, but wrapped
    dlat = (lat1 - lat0) / raster.shape[0]
    dlon = (lon1 - lon0) / raster.shape[1]
    for i, row in enumerate(row_locs):
        lons, lats = transform([row] * len(col_locs), col_locs)
        rr = ((lats - lat0) // dlat).astype(int)
        cc = ((lons - lon0) // dlon).astype(int)
        for j, (r, c) in enumerate(zip(rr, cc)):
            if 0 <= r < raster.shape[0] and 0 <= c < raster.shape[1]:
                projected[i, j] = raster[r, c]
    return projected