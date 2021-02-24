from collections import Counter
import numpy as np
import h3.api.numpy_int as h3
from h3.unstable import vect


def locs_to_h3_cnts(lons, lats, level):
    """Count occurences per H3 grid cell

    If you are pulling data from BigQuery, use the H3 functions
    there to aggregate the data, since performance will be better
    and that approach is more flexible.

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


def h3cnts_to_raster(h3_data, row_locs, col_locs, transform):
    """Convert dictionary of H3 data to raster in projected coords

    If multiple resolutions of cells are present in h3_data they
    are plotted from lowest resolution to highest resolution,
    putting the high resolution cells on top.
    
    Parameters
    ----------
    h3_data: dict mapping str to number
        Key is an H3 id, while value is the count or density at that id
    row_locs : array of float
    col_locs : array of float
    transform : function of (rows, columns) -> (lons, lats)

    Returns
    -------
    2D array of float
    """
    levels = sorted(set(h3.h3_get_resolution(h3id) for h3id in h3_data))
    raster = np.zeros([len(row_locs), len(col_locs)])
    for i, row in enumerate(row_locs):
        lons, lats = transform([row] * len(col_locs), col_locs)
        for level in levels:
            h3_indices = vect.geo_to_h3(lats, lons, level)
            for j, h3ndx in enumerate(h3_indices):
                if h3ndx in h3_data:
                    raster[i, j] = h3_data[h3ndx]
    return raster
