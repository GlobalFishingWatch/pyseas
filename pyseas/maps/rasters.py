import numpy as np

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
              origin='upper', per_km2=False): 
    """Convert a DataFrame to raster

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
    filter : function(row) -> bool, optional
        If specified only rows that return true are added to raster
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

    Returns
    -------
    np.array
    """

    # If it turns out to be useful, we could allow xyscale to be a tuple
    # rather than a scalar.
    assert origin in ['upper', 'lower']
    is_upper = (origin == 'upper')
    (min_x, max_x, min_y, max_y) = [x * xyscale for x in extent]
    columns = list(df.columns)
    x_ndx = columns.index(x_label) + 1
    y_ndx = columns.index(y_label) + 1
    v_ndx = columns.index(v_label) + 1

    ny = int(max_y - min_y)
    nx = int(max_x - min_x)
    grid = np.zeros(shape=(ny, nx), dtype=float)

    if per_km2:
        scaler = LonLat2Km2Scaler(xyscale, scale)
    else:
        scaler = LinearScalar(scale)

    for row in df.itertuples():
        xi = int(row[x_ndx] - min_x)
        yi = int((row[y_ndx] - min_y))
        if is_upper:
            yi = ny - 1 - yi
        if (0 <= xi < nx) and (0 <= yi < ny):
            grid[yi, xi] += scaler(row[x_ndx], row[y_ndx], row[v_ndx])

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
