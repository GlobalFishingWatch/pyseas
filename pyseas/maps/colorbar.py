import matplotlib.pyplot as plt
from matplotlib import gridspec
from . import core
from .. import styles


def add_colorbar(img, *, ax=None, fig=None, label='', loc='bottom', width=0.33, height=0.015, format=None, 
                 hspace=0.04, wspace=0.016, valign=0.5, right_edge=None):
    """Add colorbar to a PySeas raster

    Parameters
    ----------
    img : matplotlib Image
    ax : matplotlib Axes, optional
    fig : matplotlib Figure, optional
    label : str, optional
    loc : str, optional
        'top' or 'bottom'
    width, height : float
        Size of colorbar in Axes coordinates
    format : matplotlib formatter
        Formatter for colorbar labels.
    hspace : float, optional
        Space between colorbar and axis.
    wspace : float, optional
        Space between colorbar and label.
    valign : float, optional
        Alignment of center of text relative to colorbar.
    right_edge : float, optional
        Location of right edge of colorbar in Axes coords.

    Returns
    -------
    Colorbar
    """
    assert loc in ('top', 'bottom')
    if ax is None:
        ax = plt.gca()

    if right_edge is None:
        is_global = isinstance(core._last_projection, str) and core._last_projection.startswith('global.')
        right_edge = 0.78 if is_global else 1.0
    padded_height = height + hspace
    wloc = right_edge - width
    hloc = 0.98 + hspace if (loc == 'top') else -padded_height   

    cb_ax = ax.inset_axes([wloc, hloc, width, height], transform=ax.transAxes)
    cb = plt.colorbar(img, ax=ax, cax=cb_ax, orientation='horizontal', ticklocation=loc, format=format)

    cb_ax.text(-wspace, valign, label, transform=cb_ax.transAxes,
        fontdict=plt.rcParams.get('pyseas.map.colorbarlabelfont', styles._colorbarlabelfont),
                    horizontalalignment='right', verticalalignment='center')

    plt.sca(ax)     
    return cb_ax