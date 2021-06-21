
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib import cm
import matplotlib.pyplot as plt
from .. import props


class BivariateColormap:

    log_x = False
    log_y = False

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
        """


class TransparencyBivariateColormap(BivariateColormap):

    log_y = True

    def __init__(self, base_colormap):
        self.base_colormap = base_colormap

    # TODO: should make this parameterizable
    def __call__(self, X, Y, alpha=None):
        colors = self.base_colormap(X)
        colors[..., 3] *= Y
        if alpha is not None:
            colors[..., 3] *= alpha
        return colors



def add_bivariate_colorbox(bvcmap, xnorm=None, ynorm=None, *, ax=None, fig=None, xlabel='', ylabel='',
                xformat=None, yformat=None, loc=(1.0, 1.0), width=0.2, height=0.2,
                bg_color=None, fontsize=8):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    bvcmap : BivariateCmap
    xnorm, ynorm : matplotlib normalizer
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    xlabel, ylabel : str, optional
    xformat, yformat : str, optional
    loc : tuple of float, optional
        Location of the colormap in axis coordinates.  # TODO: add anchor
    width, height : float, options
        Size of colorbar in Axes coordinates
    bg_color : maplotlib color
    fontsize : int # TODO: stylize
    
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

    wloc, hloc = loc

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)

    x, y = np.meshgrid(np.linspace(ynorm.vmin, ynorm.vmax, 1000), 
                       np.linspace(xnorm.vmin, xnorm.vmax, 1000))

    im = cb_ax.imshow(bvcmap(ynorm(x), xnorm(y)), 
        extent=(ynorm.vmin, ynorm.vmax, xnorm.vmin, xnorm.vmax), origin='lower', aspect='auto')
    bg_color = bg_color or plt.rcParams.get('pyseas.ocean.color', props.dark.ocean.color)

    cb_ax.set_facecolor(bg_color)

    cb_ax.set_xlabel(xlabel, fontsize=fontsize)
    cb_ax.set_ylabel(ylabel, fontsize=fontsize)

    if bvcmap.log_x:
        cb_ax.set_xscale('log')
    if bvcmap.log_y:
        cb_ax.set_yscale('log')

    if xformat is not None:
        print(xformat)
        cb_ax.xaxis.set_major_formatter(xformat)
    if yformat is not None:
        print(yformat)
        cb_ax.yaxis.set_major_formatter(yformat)


    plt.sca(ax)     
    return cb_ax





def add_bivariate_raster(raster1, raster2, norm1=None, norm2=None, bvcmap=default_bvcm,
                  alpha=None, ax=None, extent=(-180, 180, -90, 90), origin='upper',
                  **kwargs):
    """Add a raster to an existing map

    Parameters
    ----------

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
    raster1 = norm1(raster1)
    if norm2 is None:
        norm2 = Normalize()
    raster2 = norm2(raster2)

    raster = bvcmap(raster1, raster2, alpha)

    return ax.imshow(raster, transform=identity,
                     extent=extent, origin=origin, **kwargs)







# def plot_raster_bv(raster1, raster2, z1min_cap, z1max_cap,
#                    subplot=(1, 1, 1), projection='global.default',
#                    bg_color=None, hide_axes=True, colorbar=None,
#                    gridlines=False, **kwargs):
#     """Draw a GFW themed map over a raster

#     Parameters
#     ----------
#     raster : 2D array
#     subplot : tuple or GridSpec
#     projection : cartopy.crs.Projection, optional
#     bg_color : str or tuple, optional
#     hide_axes : bool
#         if `true`, hide x and y axes

#     Other Parameters
#     ----------------
#     Keyword args are passed on to add_raster.

#     Returns
#     -------
#     (GeoAxes, AxesImage)
#     """
#     extent = kwargs.get('extent')
#     ax = create_map(subplot, projection, extent, bg_color, hide_axes)
#     im = add_raster_bv(raster1, raster2, z1min_cap, z1max_cap, ax=ax, **kwargs)
#     add_land(ax)
#     return ax, im


# def plot_raster_w_colorbar_bv(raster1, raster2, label='', loc='bottom',
#                               projection='global.default', hspace=0.03, wspace=0.1,
#                               vmin=None, vmax=None,
#                               bg_color=None, hide_axes=True, cbformat=None, **kwargs):
#     """Draw a GFW themed map over a raster with a colorbar

#     Parameters
#     ----------
#     raster : 2D array
#     label : str, optional
#     loc : str, optional
#     projection : cartopy.crs.Projection, optional
#     hspace : float, optional
#         space between colorbar and axis
#     wspace : float, optional
#         horizontal space adjustment
#     bg_color : str or tuple, optional
#     hide_axes : bool
#         if `true`, hide x and y axes
#     cbformat : formatter

#     Other Parameters
#     ----------------
#     Keyword args are passed on to plot_raster.

#     Returns
#     -------
#     (GeoAxes, AxesImage)
#     """
#     assert loc in ('top', 'bottom')
#     is_global = isinstance(projection, str) and projection.startswith('global.')
#     if is_global:
#         wratios = [1, 1, 1, 0.85]
#     else:
#         wratios = [1, 1, 1, 0.01]
#     if loc == 'top':
#         hratios = [.015, 1]
#         cb_ind, pl_ind = 0, 1
#         anchor = 'NE'
#     else:
#         hratios = [1, 0.08] #0.015]
#         cb_ind, pl_ind = 1, 0
#         anchor = 'SE'

#     #
#     # Get log of each grid cell in raster 1 (intensity raster)
#     # (if zero, then replace it with the minimum so that log doesn't raise an error)
#     Z1 = np.log10(raster1,
#                   out=np.ones_like(raster1) * np.log10(np.min(raster1[np.nonzero(raster1)])),
#                   where=(raster1 != 0))

#     if vmin:
#         z1min_cap = np.log10(vmin)
#     else:
#         z1min_cap = Z1.min() + 1.
#     if vmax:
#         z1max_cap = np.log10(vmax)
#     else:
#         z1max_cap = Z1.max() - 1.

#     gs = plt.GridSpec(2, 4, height_ratios=hratios, width_ratios=wratios, hspace=hspace, wspace=wspace)
#     ax, im = plot_raster_bv(raster1, raster2, z1min_cap, z1max_cap, gs[pl_ind, :], projection=projection, **kwargs)
#     ax.set_anchor(anchor)
#     cb_ax = plt.subplot(gs[cb_ind, 2])

#     #
#     # Create an empty matrix for color matrix (we need 0:101 for yy to represent 0% to 100%
#     xx, yy = np.mgrid[0:100, 0:101]

#     #
#     # For Z1 axis, it represents the intensity dimension, 0 to 1
#     # For Z2 axis, it represents the ratio dimension, 0 to 255 (from 0:red to 255:green in a colormap below)
#     Z1_plot = np.array((xx - xx.min()) / (xx.max() - xx.min()))
#     Z2_plot = np.array(255 * (yy - yy.min()) / (yy.max() - yy.min()), dtype=np.int)

#     #
#     # Two color RGBs for row ratio and high ratio
#     clow = (255, 69, 115)  # redish
#     cmid = (255, 255, 255)  # white
#     chigh = (0, 255, 195)  # greenish
#     n = 255.
#     colors = [(clow[0] / n, clow[1] / n, clow[2] / n),
#               (cmid[0] / n, cmid[1] / n, cmid[2] / n),
#               (chigh[0] / n, chigh[1] / n, chigh[2] / n)]
#     #
#     # Create a custom linear colormap using the colors above for ratio dimension (red to green)
#     cm = LinearSegmentedColormap.from_list(
#         'contrast', colors, N=256)
#     Z2_color = cm(Z2_plot)

#     #
#     # For minimum intensity, the background map color is used
#     cbg = (10, 23, 56)  # dark bluish "#0a1738"
#     cmin = (cbg[0] / n, cbg[1] / n, cbg[2] / n)  # In hex: "#0a1738"
#     Z_color = np.zeros_like(Z2_color)

#     #
#     # Generate the final color matrix by joining intensity dimension (Z1) to ratio dimension (Z2)
#     Z_color[:, :, 0] = Z2_color[:, :, 0] * Z1_plot + cmin[0] * (1 - Z1_plot)
#     Z_color[:, :, 1] = Z2_color[:, :, 1] * Z1_plot + cmin[1] * (1 - Z1_plot)
#     Z_color[:, :, 2] = Z2_color[:, :, 2] * Z1_plot + cmin[2] * (1 - Z1_plot)

#     #
#     # Plot the color matrix in the designated subplot
#     cb_ax.imshow(Z_color[:, :, 0:3], origin='lower')
#     cb_ax.set_yscale('log')
#     # cb_ax.set_ylim(10, pow(10, Z1.max()))
#     cb_ax.set_aspect('auto')
#     cb_ax.spines['top'].set_visible(False)
#     cb_ax.spines['right'].set_visible(False)
#     cb_ax.set_xlabel('Ratio of Fishing Hours by Matched Vessels to Those by All', fontsize=8)
#     cb_ax.set_ylabel('Total Fishing Hours', fontsize=8)
#     cb_ax.tick_params(labelsize=8)
#     cb_ax.set_xticklabels(cb_ax.get_xticks())
#     cb_ax.set_yticklabels(cb_ax.get_yticks())
#     labels = [str(int(float(item.get_text()))) + "%" for item in cb_ax.get_xticklabels()]
#     cb_ax.set_xticklabels(labels)
#     labels = ["", "",
#               str(round(pow(10, (z1min_cap + 1)), 1)),
#               str(round(pow(10, (z1max_cap)), 1)),
#               "", ""]
#     cb_ax.set_yticklabels(labels)
#     cb_ax.tick_params(axis="x", direction="in", pad=1)

#     leg_ax = plt.subplot(gs[cb_ind, 1], frame_on=False)
#     leg_ax.axes.get_xaxis().set_visible(False)
#     leg_ax.axes.get_yaxis().set_visible(False)
#     leg_ax.text(0.8, 0.5, label,
#         fontdict=plt.rcParams.get('pyseas.map.colorbarlabelfont', styles._colorbarlabelfont),
#                     horizontalalignment='right', verticalalignment='center', fontsize=10)
#     if loc == 'top':
#         cb_ax.xaxis.tick_top()
#     plt.sca(ax)

#     return ax, im, cb_ax