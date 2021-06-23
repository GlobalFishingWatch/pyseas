
import numpy as np
from matplotlib.colors import Normalize, LogNorm
from matplotlib import cm
import matplotlib.pyplot as plt
from . import core
from .. import props


class BivariateColormap:

    log_x = None
    log_y = None

    def __call__(self, X, Y, alpha=None):
        """Return color for the pair of values X and Y.

        Parameters
        ----------
        X, Y : float or np.array of float
            Each pair of X, Y values is mapped to a color value.
            The data should be in the range [0.0, 1.0].
        alpha : float or np.array or float
            A scalar in the range [0.0, 1.0] that specifies the 
            opacity at each X, Y pair. If alpha is an array, it 
            must match the shape of X and Y.   

        Return
        ------
        np.array
            The shape will be np.shape(X) + (4,) to accommodate RGBA
            information.       
        """


class TransparencyBivariateColormap(BivariateColormap):
    """Bivariate colormap combining standard colormap with transparency

    The first value (`X`) is looked up in `base_cmap` and the result is
    multiplied by the second value ('Y').

    Parameters
    ----------
    base_cmap : matplotlib Colormap
    log_x, log_y : bool, optional
    """

    def __init__(self, base_cmap, log_x=None, log_y=None):
        self.base_cmap = base_cmap
        self.log_x = log_x
        self.log_y = log_y

    # TODO: should make this parameterizable
    def __call__(self, X, Y, alpha=None):
        colors = self.base_cmap(X)
        colors[..., 3] *= Y
        if alpha is not None:
            colors[..., 3] *= alpha
        return colors


class SummedBivariateColormap(BivariateColormap):
    """Bivariate colormap summing two standard colormaps

    The colors for `X` and `Y` are looked up in `cmap1` and `cmap2`
    respectively and then their values are summed and clipped to the
    range [0, 1]. 

    N.B., the two colormaps should be chosen to be compatible with each
    other, e.g. Reds and Blues or this will not work well.

    Parameters
    ----------
    cmap1, cmap2 : matplotlib colormap
    """

    def __init__(self, cmap1, cmap2):
        self.cmap1 = cmap1
        self.cmap2 = cmap2

    # TODO: should make this parameterizable
    def __call__(self, X, Y, alpha=None):
        clr1 = self.cmap1(X)
        clr2 = self.cmap2(Y)
        # TODO: Do we want to check for Nan here?
        colors = np.clip(clr1 + clr2, 0, 1)
        if alpha is not None:
            colors[..., 3] *= alpha
        return colors        


_default_cmap = SummedBivariateColormap(cm.Reds, cm.Blues)


def _loc_finder(loc_name, width, height, pad):
    if loc_name == 'below right':
        return 1 - width, -(height + pad)
    if loc_name == 'lower right':
        return 1 + pad, 0
    if loc_name == 'upper right':
        return 1 + pad, 1 - height
    if loc_name == 'above right':
        return 1 - width, 1 + pad
    raise ValueError(f'unknown loc_name: {loc_name}')


# TODO: in proj_info
# Or figure out how to get aspect ratios efficiently and accurately
hw_ratio_map = {
    'global.default' : 2,
    'global.dateline_centered' : 2,
    'global.pacific_centered' : 2,
    'global.atlantic_centered' : 2,
    'global.indian_centered' : 2,
    'regional.north_pacific' : 1.9,
}


def _is_log(cmap_value, norm):
    if cmap_value is None:
        return isinstance(norm, LogNorm)
    else:
        return cmap_value


def add_bivariate_colorbox(bvcmap, xnorm=None, ynorm=None, *, ax=None, fig=None, xlabel='', ylabel='',
                xformat=None, yformat=None, loc='below right', width=None, height=None,
                bg_color=None, fontsize=8, pad=0.05):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    bvcmap : BivariateCmap
    xnorm, ynorm : matplotlib normalizer
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    xlabel, ylabel : str, optional
    xformat, yformat : str, optional
    loc : str or tuple of float, optional
        Location name or ocation of the colorbox in axis coordinates.  
        Currently supported names are 'below right', 'lower right', 'upper right',
        and 'above right'.
    width, height : float, optional
        Size of colorbar in Axes coordinates
    bg_color : maplotlib color, optional
    fontsize : int, optional # TODO: stylize
    pad : float, optional
    
    Returns
    -------
    Axes
    """
    if ax is None:
        ax = plt.gca()
    if xnorm is None:
        xnorm = Normalize(vmin=0, vmax=1, clip=True)
    if ynorm is None:
        ynorm = Normalize(vmin=0, vmax=1, clip=True)
    if width is height is None:
        width = 0.2

    if height is None:
        height = width * hw_ratio_map.get(core._last_projection, 1)
    if width is None:
        width = height / hw_ratio_map.get(core._last_projection, 1)

    if isinstance(loc, str):
        loc = _loc_finder(loc, width, height, pad=pad)

    wloc, hloc = loc

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)

    x, y = np.meshgrid(np.linspace(xnorm.vmin, xnorm.vmax, 1000), 
                       np.linspace(ynorm.vmin, ynorm.vmax, 1000))

    im = cb_ax.imshow(bvcmap(xnorm(x), ynorm(y)), 
        extent=(xnorm.vmin, xnorm.vmax, ynorm.vmin, ynorm.vmax), origin='lower', aspect='auto')
    bg_color = bg_color or plt.rcParams.get('pyseas.ocean.color', props.dark.ocean.color)

    cb_ax.set_facecolor(bg_color)

    cb_ax.set_xlabel(xlabel, fontsize=fontsize)
    cb_ax.set_ylabel(ylabel, fontsize=fontsize)

    if _is_log(bvcmap.log_x, xnorm):
        cb_ax.set_xscale('log')
    if _is_log(bvcmap.log_y, ynorm):
        cb_ax.set_yscale('log')

    if xformat is not None:
        cb_ax.xaxis.set_major_formatter(xformat)
    if yformat is not None:
        cb_ax.yaxis.set_major_formatter(yformat)


    plt.sca(ax)     
    return cb_ax



def add_bivariate_raster(raster1, raster2, bvcmap=_default_cmap, norm1=None, norm2=None, *,
                  alpha=None, ax=None, extent=(-180, 180, -90, 90), origin='upper',
                  **kwargs):
    """Add a raster to an existing map

    Parameters
    ----------
    raster1, raster2 : np.array
    bvcmap : BivariateCmap
    norm1, norm2 : matplotlib normalization
    alpha : array or float, optional
        Must be broadcastable to the shape of the rasters.
    ax : Axes, optional
    extent : tuple of 4 floats, optional
    origin : 'upper' or 'lower', optional

    Other Parameters
    ----------------
    Keyword args are passed on to imshow.

    Returns
    -------
    AxesImage
    """
    if ax is None:
        ax = plt.gca()
    if norm1 is None:
        norm1 = Normalize()
    if norm2 is None:
        norm2 = Normalize()

    raster = bvcmap(norm1(raster1), norm2(raster2), alpha)

    return core.add_raster(raster, extent=extent, origin=origin, **kwargs)