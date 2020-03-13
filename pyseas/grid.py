import numpy as np


def df2raster(df, x_label, y_label, v_label, xyscale, 
            vscale=1, extent=(-180, 180, -90, 90), 
            filter=None, origin='upper'): 
    """Convert a DataFrame to raster

    Parameters
    ----------
    df : DataFrame
    x_label : str
    y_label : str
    v_label : str
        Label for the value column
    xyscale : float
        How many raster points per unit in x and y. Relates 
        `x` and `y` values to `extent`.
    vscale: float, optional
        Scale the output by this amount
    extent : tuple of float, optional
        (min_x, max_x, min_y, max_y)
    filter : function(row) -> bool, optional
        If specified only rows that return true are added to raster
    origin : 'upper' | 'lower'
        Whether to to produce a raster with the origin at the upper left
        or at the lower left.

    Returns
    -------
    np.array
    """

    # TODO: xyscale can be tuple
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

    for row in df.itertuples():
        xi = int(row[x_ndx] - min_x)
        yi = int((row[y_ndx] - min_y))
        if is_upper:
            yi = ny - 1 - yi
        if (0 <= xi < nx) and (0 <= yi < ny):
            if filter and not filter(row):
                continue
            grid[yi, xi] += row[v_ndx]

    return grid * vscale