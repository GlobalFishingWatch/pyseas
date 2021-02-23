from collections import Counter
import numpy as np
import h3.api.numpy_int as h3
from h3.unstable import vect


def locs_to_h3cnts(lons, lats, level):
    """Count occurences per H3 grid cell
    
    Parameters
    ----------
    df : pd.DataFrame
        Should have lat and lon columns.
    level : int
        H3 level as specified at https://h3geo.org/docs/core-library/restable.
        Level 8 corresponds to 0.75 km2 and works for relatively fine scale features.
    
    Returns
    -------
    dict
        Maps H3 index values to counts
    """
    counts = dict()
    h3_indices = vect.geo_to_h3(lats.astype('double'), lons.astype('double'), level)
    for ndx in h3_indices:
        if ndx not in counts:
            counts[ndx] = 0
        counts[ndx] += 1
    return counts


def h3cnts_to_raster(h3cnts, xvals, yvals, transform):
    """Convert dictionary of h3cnts to raster

    TODO: discuss how it plots from low resolution to
    high resolution
    
    Parameters
    ----------
    h3cnts: dict mapping str to number
        Key is an h3id, while value is the count at that id
    xvals : array of float
    yvals : array of float
    transform : function mapping array of (x, y) to array of (lon, lat)

    Returns
    -------
    2D array of float
    """
    levels = sorted(set(h3.h3_get_resolution(h3id) for h3id in h3cnts))
    raster = np.zeros([len(yvals), len(xvals)])
    for i, y in enumerate(yvals):
        lons, lats = np.transpose(transform([(x, y) for x in xvals]))
        for level in levels:
            h3_indices = vect.geo_to_h3(lats, lons, level)
            for j, h3ndx in enumerate(h3_indices):
                if h3ndx in h3cnts:
                    raster[i, j] = h3cnts[h3ndx]
    return raster
