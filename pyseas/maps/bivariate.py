import numpy as np
from matplotlib.colors import Normalize, LogNorm, LinearSegmentedColormap, Colormap
import matplotlib.pyplot as plt
import warnings
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

    @staticmethod
    def discretize(x, n):
        if n is None:
            return x
        else:
            return np.minimum(np.floor(x * n) / (n - 1), 1)


class TransparencyBivariateColormap(BivariateColormap):
    """Bivariate colormap combining standard colormap with transparency

    The first value (`X`) is looked up in `base_cmap` and the result is
    multiplied by the second value ('Y').

    Parameters
    ----------
    base_cmap : matplotlib Colormap
    log_x, log_y : bool, optional
    """

    def __init__(self, cmap, transmap=None, log_x=None, log_y=None, n_x=None, n_y=None):
        self.cmap = cmap
        self.transmap = (lambda x: x) if (transmap is None) else transmap
        self.log_x = log_x
        self.log_y = log_y
        self.n_x = n_x
        self.n_y = n_y

    def __call__(self, X, Y, alpha=None):
        colors = self.cmap(self.discretize(X, self.n_x))
        colors[..., 3] *= self.transmap(self.discretize(Y, self.n_y))
        if alpha is not None:
            colors[..., 3] *= alpha
        return colors


class MergeBivariateColormap(BivariateColormap):
    """Bivariate colormap maximizing two standard colormaps

    The colors for `X` and `Y` are looked up in `cmap1` and `cmap2`
    respectively and then merged using `merge_colors`

    Parameters
    ----------
    cmap1, cmap2 : matplotlib colormap
    bad_color : tuple of float
        Can be length 3 (RGB) or 4 (RGBA)
    log_x, log_y : bool, optional
        Hints for bivariate colorbox
    n_x, n_y : int or None, optional
        If specified discretize the colormap into n bins.
    """

    def __init__(
        self,
        cmap1,
        cmap2,
        bad_color=(0, 0, 0, 0),
        log_x=None,
        log_y=None,
        n_x=None,
        n_y=None,
    ):
        self.cmap1 = cmap1
        self.cmap2 = cmap2
        self.bad_color = bad_color
        self.log_x = log_x
        self.log_y = log_y
        self.n_x = n_x
        self.n_y = n_y

    def __call__(self, X, Y, alpha=None):
        mask = np.isnan(X) | np.isnan(Y)
        clr1 = self.cmap1(self.discretize(X, self.n_x))
        clr2 = self.cmap2(self.discretize(Y, self.n_y))
        colors = self.merge_colors(clr1, clr2)
        colors[mask] = self.bad_color
        if alpha is not None:
            colors[..., 3] *= alpha
        return colors

    def merge_colors(self, c1, c2):
        raise NotImplementedError


class MaxBivariateColormap(MergeBivariateColormap):
    def merge_colors(self, c1, c2):
        return np.maximum(c1, c2)


class MinBivariateColormap(MergeBivariateColormap):
    def merge_colors(self, c1, c2):
        return np.minimum(c1, c2)


_lime = LinearSegmentedColormap.from_list(
    "lime", np.array([(243, 243, 243), (100, 255, 135)]) / 255.0
)
_pink = LinearSegmentedColormap.from_list(
    "pink", np.array([(243, 243, 243), (255, 123, 169)]) / 255.0
)
_default_cmap = MinBivariateColormap(_lime, _pink)


def _loc_finder(loc_name, width, height, pad):
    if loc_name == "below right":
        return 1 - width, -(height + pad)
    if loc_name == "lower right":
        return 1 + pad, 0
    if loc_name == "upper right":
        return 1 + pad, 1 - height
    if loc_name == "above right":
        return 1 - width, 1 + pad
    raise ValueError(f"unknown loc_name: {loc_name}")


def _is_log(cmap_value, norm):
    if cmap_value is None:
        return isinstance(norm, LogNorm)
    else:
        return cmap_value


def _setup_width_and_height(width, height, aspect_ratio):
    if width is height is None:
        width = 0.2
    if aspect_ratio is None:
        aspect_ratio = 1.0

    if width is None or height is None:
        if core._last_projection in core.projection_info:
            scale = (
                core.projection_info[core._last_projection]["aspect_ratio"]
                / aspect_ratio
            )
        else:
            warnings.warn(
                "Using non-standard projection, consider setting width and height"
            )
            scale = 1 / aspect_ratio

        if height is None:
            height = width * scale
        if width is None:
            width = height / scale

    return width, height


def _locs(vmin, vmax, pixels, islog):
    if islog:
        return np.exp(np.linspace(np.log(vmin), np.log(vmax), pixels))
    else:
        return np.linspace(vmin, vmax, pixels)


class _IndexColormap(Colormap):
    def __init__(self, source):
        self.source = np.asarray(source)

    def __call__(self, x, alpha=None, bytes=False):
        return self.source[x]


class _IdentNorm(Normalize):
    def __call__(self, x):
        return x


def add_bivariate_colorbox(
    bvcmap,
    xnorm=None,
    ynorm=None,
    *,
    ax=None,
    fig=None,
    xlabel="",
    ylabel="",
    xformat=None,
    yformat=None,
    loc="below right",
    width=None,
    height=None,
    aspect_ratio=None,
    bg_color=None,
    fontsize=8,
    pad=0.05,
    pixels=256,
):
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
        Location name or location of the colorbox in axis coordinates.
        Currently supported names are 'below right', 'lower right', 'upper right',
        and 'above right'.
    width, height : float or None, optional
        Size of colorbar in Axes coordinates. If only one is specified and the last
        projection was one of the standard one, then an appropriate aspect ratio will
        be used. Otherwise the same width and height will be used.
    aspect_ratio : float or None, optional
    bg_color : maplotlib color, optional
    fontsize : int, optional
    pad : float, optional
    pixels : int, optional
        Number of pixels along in each axis in the colorbox image.

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
    width, height = _setup_width_and_height(width, height, aspect_ratio)
    if isinstance(loc, str):
        loc = _loc_finder(loc, width, height, pad=pad)
    wloc, hloc = loc

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)

    islog_x = _is_log(bvcmap.log_x, xnorm)
    islog_y = _is_log(bvcmap.log_y, ynorm)

    x = _locs(xnorm.vmin, xnorm.vmax, pixels, islog_x)
    y = _locs(ynorm.vmin, ynorm.vmax, pixels, islog_y)

    xmg, ymg = np.meshgrid(
        x,
        y,
    )

    # We use pcolormesh, with this hacked colormap so that we get even points
    # in axes space even when we have log axes. If we use imshow instead,
    # points get further and further apart for small log values.
    icmap = _IndexColormap(bvcmap(xnorm(xmg), ynorm(ymg)).reshape(-1, 4))
    cb_ax.pcolormesh(
        x,
        y,
        np.arange(pixels * pixels).reshape(pixels, pixels),
        cmap=icmap,
        norm=_IdentNorm(),
    )

    bg_color = bg_color or plt.rcParams.get(
        "pyseas.ocean.color", props.dark.ocean.color
    )

    cb_ax.set_facecolor(bg_color)

    cb_ax.set_xlabel(xlabel, fontsize=fontsize)
    cb_ax.set_ylabel(ylabel, fontsize=fontsize)

    if islog_x:
        cb_ax.set_xscale("log")
    if islog_y:
        cb_ax.set_yscale("log")

    if xformat is not None:
        cb_ax.xaxis.set_major_formatter(xformat)
    if yformat is not None:
        cb_ax.yaxis.set_major_formatter(yformat)

    plt.sca(ax)
    return cb_ax


def add_bivariate_raster(
    raster1,
    raster2,
    bvcmap=_default_cmap,
    norm1=None,
    norm2=None,
    *,
    alpha=None,
    ax=None,
    extent=(-180, 180, -90, 90),
    origin="upper",
    **kwargs,
):
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

    return core.add_raster(raster, ax=ax, extent=extent, origin=origin, **kwargs)
