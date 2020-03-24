import numpy as np
import pandas as pd


def asarray(x, dtype=None):
    if isinstance(x, pd.Series):
        x = x.values
    return np.asarray(x, dtype=dtype)

