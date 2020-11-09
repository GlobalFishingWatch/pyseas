import numpy as np
import pandas as pd


def asarray(x, dtype=None):
    if isinstance(x, pd.Series):
        x = x.values
    return np.asarray(x, dtype=dtype)


def lon_avg(lons):
    """Return average lon using sin/cos averaging

    Parameters
    ----------
    lons: array of float
        longitudes in degrees

    Returns
    -------
    float, average longitude in degrees
    """
    coslon = np.mean(np.cos(np.radians(lons)))
    sinlon = np.mean(np.sin(np.radians(lons)))
    return np.degrees(np.arctan2(sinlon, coslon))



def is_sorted(values):
    """Returns True if sequence is sorted else False"""
    is_first = True
    for x in values:
        if is_first:
            is_first = False
        elif x < last:
            return False
        last = x
    return True

