"""Rasterize lat-lon rasters H3 DGG data in a way that works well for mapping.

Plotting rasters using `imshow` on Cartopy maps does not work well with high
resolution maps. Fine details can disappear or become coarse and blocky.
Plotting using `interpolation="nearest"` helps some with this, but still
results in loss of detail. The functions in this module render rasters and
H3 data to Cartopy GeoAxes with improved results.

The two main entry points in the module are `raster_show` and `h3_show`. 
`raster_show` has the same interface as `imshow`. `h3_show` is similar
except it accepts H3 Discrete Global Grid data.

In both cases, the strategy is to generate a raster in *display* coordinates,
interpolating the data in the raster or DGG grid directly onto the new
raster. In order to get the correct display coordinates, it is necessary
to subclass `AxesImage` and have it do the interpolation when the map
is drawn. Since the interpolated array is already in display
coordinates, no projection is applied when it is drawn and this removes
the blockiness and loss of detail that plague rendering with `imshow`.

Much code here repurposed from the matplotlib sources for `Axes.imshow` and
`AxesImage`.

"""
from collections import Counter
import numpy as np
import h3.api.numpy_int as h3

from matplotlib.image import AxesImage
from matplotlib import rcParams
from matplotlib import cm
import matplotlib.cbook as cbook
import matplotlib.artist as martist
import warnings

from . import core


def h3_show(ax, h3_data, cmap=None, norm=None, aspect=None, 
            vmin=None, vmax=None, url=None, alpha=1.0, **kwargs):
    """Plot H3 DGG data in a way friendly to projected maps.

    This is derived from Axes.imshow.

    Parameters
    ----------
    ax : matplotlib Axes
    h3_data : dict mapping np.uint64 to int or float
        The key is a H3 ID, while the value is either a count or density.
    cmap, norm, aspect, vmin, vmax, url, alpha, kwargs : see Axes.imshow

    Returns
    -------
    H3Image instance
    """
    norm = _setup_show(ax, aspect, norm, vmin, vmax)

    im = H3Image(ax, cmap=cmap, norm=norm, extent=ax.get_extent(), interpolation='nearest', 
                 origin='lower', **kwargs)

    return _finalize_show(h3_data, im, ax, alpha, url)


def raster_show(ax, raster, extent, origin='upper', cmap=None, norm=None, aspect=None, 
            vmin=None, vmax=None, url=None, alpha=1.0, **kwargs):
    """
    Plot raster data in a way friendly to projected maps.

    This is derived from Axes.imshow.

    Parameters
    ----------
    ax : matplotlib Axes
    raster : 2D array of float
    extent : 4-tuple of floats
        The bounds of the raster as (lon0, lon1, lat0, lat1)
    origin : 'upper' or 'lower'
        Whether to place the y-origin at the top or bottom of the axes
    cmap, norm, aspect, vmin, vmax, url, alpha, kwargs : see Axes.imshow

    Returns
    -------
    RasterImage instance
    """
    norm = _setup_show(ax, aspect, norm, vmin, vmax)

    im = RasterImage(ax, cmap=cmap, norm=norm, extent=ax.get_extent(), interpolation='nearest', 
        origin='lower', **kwargs)

    return _finalize_show((raster, extent, origin), im, ax, alpha, url)


def _setup_show(ax, aspect, norm, vmin, vmax):
    """Common setup code for show_raster and show_h3"""
    if aspect is None:
        aspect = rcParams['image.aspect']
    ax.set_aspect(aspect)
    if norm is not None:
        assert vmin is vmax is None
    if norm is None:
        norm = Normalize(vmin, vmax)
    return norm


def _finalize_show(source_data, im, ax, alpha, url):
    """Common finalization code for show_raster and show_h3"""
    im.set_data(source_data)
    im.set_alpha(alpha)
    if im.get_clip_path() is None:
        # image does not already have clipping set, clip to axes patch
        im.set_clip_path(ax.patch)
    im.set_url(url)
    # update ax.dataLim, and, if autoscaling, set viewLim
    # to tightly fit the image, regardless of dataLim.
    im.set_extent(im.get_extent())
    ax.add_image(im)
    return im


def h3cnts_to_raster(h3_data, row_locs, col_locs, transform):
    """Convert dictionary of H3 data to raster in projected coords

    If multiple resolutions of cells are present in h3_data they
    are plotted from lowest resolution to highest resolution,
    putting the high resolution cells on top.

    Note that this relies on `h3.unstable`, so might require
    modification to work in the future.
    
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
    # Delay importation of vect, so only get the warning when actually used.
    with warnings.catch_warnings():
        # Suppress useless UserWarning about unstable
        warnings.simplefilter("ignore")            
        from h3.unstable import vect

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
    counts = np.zeros([len(row_locs), len(col_locs)]) + 1e-10
    lon0, lon1, lat0, lat1 = extent
    if origin == 'upper':
        lat0, lat1 = lat1, lat0
    # TODO: Support second value > first, assuming rightward, but wrapped
    dlat = (lat1 - lat0) / raster.shape[0]
    dlon = (lon1 - lon0) / raster.shape[1]

    ii = np.empty(len(col_locs), dtype=int)
    jj = np.arange(len(col_locs), dtype=int)

    for i, row in enumerate(row_locs):
        lons, lats = transform([row] * len(col_locs), col_locs)
        rr = ((lats - lat0) // dlat + 0.5).astype(int)
        cc = ((lons - lon0) // dlon + 0.5).astype(int)

        valid = (0 <= rr) 
        valid &= (rr < raster.shape[0])
        valid &= (0 <= cc)
        valid &= (cc < raster.shape[1])

        ii.fill(i) 

        projected[ii[valid], jj[valid]] += raster[rr[valid], cc[valid]]
        counts[ii[valid], jj[valid]] += 1

    return projected / counts


class InterpImage(AxesImage):

    def update_A(self):
        """Update the array data"""
        rr, cc, tx, dext = setup_composite_tx(self._axes)
        A = self._get_updated_A(rr, cc, tx)
        cm.ScalarMappable.set_array(self, cbook.safe_masked_invalid(A, copy=True))
        self._scale_norm(self.norm, None, None)
        self.set_extent(dext)

    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        """Draw the image, updating the array data if stale"""
        if self.stale:
            self.update_A()
        super().draw(renderer, *args, **kwargs)

    def set_data(self, source_data):
        """Set the source data for the image"""
        self._source_data = source_data
        self.stale = True


class H3Image(InterpImage):
    """Image that uses H3 data as its source and plots well on projected maps.

    Typically used through `h3_show`.
    """
    def _get_updated_A(self, rr, cc, tx):
        return h3cnts_to_raster(self._source_data, rr, cc, tx) 


class RasterImage(InterpImage):
    """Image that uses raster data as its source and plots well on projected maps.

    Typically used through `raster_show`.
    """
    def _get_updated_A(self, rr, cc, tx):
        raster, extent, origin = self._source_data
        return raster_to_raster(raster, extent, rr, cc, tx, origin=origin)


def setup_composite_tx(ax):
    """Return composite transform and auxiliary values

    Parameters
    ----------
    ax : matplotlib Axes

    Returns
    -------
    numpy array or row locations in output raster
    numpy array of column locations in output raster
    function of (rows, columns) -> (lons, lats)
    extent of coordinate range in data coordinates
    """
    (i0, j0), (i1, j1) = ax.transAxes.transform([(0, 0), (1, 1)])
    i0, j0 = (np.floor(x) for x in (i0, j0))
    i1, j1 = (np.ceil(x) for x in (i1, j1))
    col_locs = np.arange(i0, i1)
    row_locs = np.arange(j0, j1)
    (e_i0, e_j0), (e_i1, e_j1) = ax.transData.inverted().transform([(i0, j0), (i1, j1)])
    display_extent = (e_i0, e_i1, e_j0, e_j1)
    def composite_tx(rr, cc):
        # rr, cc -> lons, lats
        cr = list(zip(cc, rr))
        data_crds = np.asarray(ax.transData.inverted().transform(cr))
        lonlat = core.identity.transform_points(ax.projection, 
                                        data_crds[:, 0], data_crds[:, 1])[:, :2]
        return np.transpose(lonlat)
    return row_locs, col_locs, composite_tx, display_extent



