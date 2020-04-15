
import pytest
import pandas as pd
import numpy as np
from pyseas.maps import rasters


def test_uniform():
    scale = 4
    lon_bin_template = np.arange(-180 * scale, 180 * scale)
    lat_bin_template = np.arange(-90 * scale, 90 * scale)
    lon_bin, lat_bin = [x.flatten() for x in np.meshgrid(lon_bin_template, lat_bin_template, indexing='ij')]
    km_per_deg = 111
    values = np.cos(np.radians(lat_bin / scale)) / (scale ** 2) * (km_per_deg ** 2)
    df = pd.DataFrame({'lon_bin' : lon_bin, 'lat_bin' : lat_bin, 'values' : values})
    raster = rasters.df2raster(df, 'lon_bin', 'lat_bin', 'values', 
                                     xyscale=scale, origin='lower', per_km2=True)
    np.allclose(raster, 2.0, atol=0.001)
