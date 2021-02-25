from collections import Counter
import numpy as np
import h3.api.numpy_int as h3
from h3.unstable import vect

from matplotlib.image import AxesImage
from matplotlib import rcParams
from matplotlib import cm
import matplotlib.cbook as cbook
import matplotlib.artist as martist

from . import core


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


class H3Image(AxesImage):

    def update_A(self):
        rr, cc, tx = setup_composite_tx(self._axes)
        A = h3cnts_to_raster(self._h3_data, rr, cc, tx) 
        cm.ScalarMappable.set_array(self,
                                    cbook.safe_masked_invalid(A, copy=True))
        self._scale_norm(self.norm, None, None)

    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        if self.stale:
            self.update_A()
        super().draw(renderer, *args, **kwargs)


    def set_data(self, h3_data):
        self._h3_data = h3_data
        self.stale = True


def h3_show(ax, h3_data, cmap=None, norm=None, aspect=None, 
            vmin=None, vmax=None, url=None, alpha=1.0, **kwargs):
    if aspect is None:
        aspect = rcParams['image.aspect']
    ax.set_aspect(aspect)
    extent = ax.get_extent()
    # TODO: interp / origin should happen in H3imag
    im = H3Image(ax, cmap=cmap, norm=norm, extent=extent, interpolation='nearest', 
        origin='lower', **kwargs)

    im.set_data(h3_data)
    im.set_alpha(alpha)
    if im.get_clip_path() is None:
        # image does not already have clipping set, clip to axes patch
        im.set_clip_path(ax.patch)
    if norm is not None:
        assert vmin is vmax is None
    if norm is None:
        norm = Normalize(vmin, vmax)
    im.set_url(url)

    # update ax.dataLim, and, if autoscaling, set viewLim
    # to tightly fit the image, regardless of dataLim.
    im.set_extent(im.get_extent())

    ax.add_image(im)
    return im


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