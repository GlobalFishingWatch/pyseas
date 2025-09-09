import numpy as np
import pandas as pd

KM_PER_DEG_LAT = 110.574
KM_PER_DEG_LON0 = 111.320

# Add test
class LonLat2Km2Scaler(object):

    def __init__(self, xyscale, scale=1):
        self.xyscale = xyscale
        self.scale = scale
        self._scale0 = KM_PER_DEG_LAT * KM_PER_DEG_LON0 / xyscale ** 2

    def __call__(self, x, y, v):
        return self.scale * v / (np.cos(np.radians(y / self.xyscale)) * self._scale0)



class LinearScalar(object):

    def __init__(self, scale):
        self.scale = scale

    def __call__(self, x, y, v):
        return self.scale * v



def df2raster(df, x_label, y_label, v_label, xyscale,
              scale=1, extent=(-180, 180, -90, 90),
              origin='upper', per_km2=False, fill=0.0):
    """
    Convert a DataFrame to raster.

    Parameters
    ----------
    df : DataFrame
    x_label : str
        Label in the dataframe containing the x-values. These values should be integers
        specifying the relative pixel position in the raster. However they do not need
        to be positive. Typically these values are produced from a query similar to
        `SELECT CAST(lon * SOME_SCALE AS INT) AS x_values`
    y_label : str
        Label in the dataframe containing the y-values. See `x_label`
    v_label : str
        Label for the value column
    xyscale : float
        How many raster points per degree in x and y.
    scale: float or func, optional
        Scale the output by this amount
    extent : tuple of float, optional
        (min_x, max_x, min_y, max_y)
    origin : 'upper' | 'lower', optional
        Whether to to produce a raster with the origin at the upper left
        or at the lower left.
    per_km2 : bool, optional
        If True, inputs are assumed to be per grid cell where
        each side is 1/`xyscale` degrees. Output is scaled to per km2, 
        then scaled using `scale`.  The primary purpose of this 
        adjustment is to correct for the varying sizes of grid cells
        by latitude. Note that this is not appropriate for quantities
        such as reception quality that do not scale with area.
    fill : float, optional
        Fill the grid cells that have no corresponding values in the 
        dataframe with this value. Defaults to zero. Can be helpful to
        specify fill=np.nan for gridded data with missing values.

    Returns
    -------
    np.ndarray
    """
    if origin not in ('upper','lower'):
        raise ValueError(f"origin must be 'upper' or 'lower', got {origin!r}")

    is_upper = (origin == 'upper')
    min_x, max_x, min_y, max_y = [x * xyscale for x in extent]
    ny = int(max_y - min_y)
    nx = int(max_x - min_x)

    grid = np.full((ny, nx), np.nan, dtype=float)

    scaler = LonLat2Km2Scaler(xyscale, scale) if per_km2 else LinearScalar(scale)

    cols = list(df.columns)
    xi_col = cols.index(x_label) + 1
    yi_col = cols.index(y_label) + 1
    vi_col = cols.index(v_label) + 1

    for row in df.itertuples():
        xi = int(row[xi_col] - min_x)
        yi = int(row[yi_col] - min_y)
        if is_upper:
            yi = ny - 1 - yi
        if 0 <= xi < nx and 0 <= yi < ny:
            val = scaler(row[xi_col], row[yi_col], row[vi_col])
            if pd.isna(grid[yi, xi]):
                grid[yi, xi] = val
            elif pd.notna(val):
                grid[yi, xi] += val

    if fill is not None:
        grid = np.where(np.isnan(grid), fill, grid)

    return grid


def locs_to_h3_cnts(lons, lats, level):
    """Count occurrences per H3 grid cell

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
